"""Immutable future-course proposals; acceptance creates a separately pending archive."""
import copy
import shutil
import tempfile
from pathlib import Path
import omni_core as c
import omni_learning_store as store
import omni_quiz as q
from omni_quiz_schema import require, text, identifier


def binding(root):
    state=c.read(root/'state.json');c.check_approval(root,state);c.check_deliveries(root,state)
    return {'config':c.digest(root/'config.json'),'plan':c.digest(root/'plan.json'),'delivered':store.fingerprint(state['lessons'])}


def validate_evidence(root, data):
    require(data['basis'] in ('user_request','assessment') and isinstance(data['evidence'],list), 'Proposal needs an explicit user_request or assessment basis.')
    require(data['basis']!='assessment' or bool(data['evidence']), 'Assessment-based changes need actual answer/grade evidence.')
    for ref in data['evidence']:
        require(isinstance(ref,dict) and set(ref)=={'attempt_id','question_id','answer_id','grade_id'}, 'Use exact current assessment references.')
        _,attempt,definition=q.load_attempt(root,ref['attempt_id']);question=q.question_for(definition,ref['question_id']);state=q.qstate(attempt,question)
        require(state['answer'] and state['grade'] and state['answer']['id']==ref['answer_id'] and state['grade']['id']==ref['grade_id'], 'Proposal evidence is missing or superseded; inspect the latest feedback and propose again.')
        require(state['grade']['feedback']['verdict'] not in ('needs_review','withdrawn'), 'Resolve disputed evidence before using it for course changes.')
        from omni_study import derived
        item_id='r_'+store.fingerprint({'quiz':attempt['quiz_hash'],'question':ref['question_id']})[:24]
        item=next(x for x in derived(root) if x['id']==item_id)
        require(item['judgment'] not in ('clarify','withdrawn') and not item['retired'], 'This frozen question has unresolved or retired evidence; inspect the profile before proposing changes.')


def validate(root,data):
    require(isinstance(data,dict) and set(data)=={'id','reason','basis','evidence','config','plan'}, 'Proposal needs id, reason, basis, evidence, complete future config and plan.')
    identifier(data['id']);require(text(data['reason']), 'Retain the actual reason for adjusting future learning.')
    c.validate_config(data['config']);c.validate_plan(data['plan'])
    old=c.read(root/'config.json')
    require(data['config'].get('delivery')==old.get('delivery'), 'Destination changes use the separate connection/approval flow, not a pace revision.')
    validate_evidence(root,data)
    figure=data['plan'].get('figure',{})
    asset=Path(figure.get('path',''))
    require(not asset.is_absolute() and asset.parts and '..' not in asset.parts, 'Future plan figure must be a local path.')
    source=root/asset
    require(source.is_file() and source.resolve().is_relative_to(root) and not source.is_symlink(), 'Review the future plan image inside the original course first.')
    if data['config'].get('textbook'):
        from omni_textbooks import validate_figure
        validate_figure(root,data['config'],figure,data['plan'].get('sources',[]))
    else:
        require(asset.parts[0]=='assets', 'Future plan figure must be a local assets path.')
    if data['config'].get('materials'):
        from omni_materials import verify_selection
        for selection in data['config']['materials']['selections']:verify_selection(root,selection)
    return source


def propose(root,data):
    root=Path(root).resolve()
    with c.lock(root):
        asset=validate(root,data);value={'proposal':copy.deepcopy(data),'binding':binding(root),'asset_hash':c.digest(asset)}
        digest=store.fingerprint(value);target=store.path(root,'proposals',data['id']+'.json')
        if target.exists():require(c.read(target)['hash']==digest, 'Immutable proposal ID exists; create a new proposal.')
        else:store.save(root,('proposals',target.name),dict(value,hash=digest,created_at=q.stamp()))
        return inspect(root,data['id'])


def inspect(root,proposal_id):
    identifier(proposal_id);value=c.read(store.path(root,'proposals',proposal_id+'.json'))
    require(value['hash']==store.fingerprint({k:v for k,v in value.items() if k not in ('hash','created_at')}), 'Proposal changed; preserve history and prepare a new proposal.')
    return value


def apply(root,proposal_id,destination,consent):
    root=Path(root).resolve();destination=Path(destination).absolute()
    require(text(consent), 'Acceptance needs the actual learner confirmation after reviewing the full proposal.')
    require(not destination.is_symlink(), 'New course destination cannot be a symlink.')
    destination=destination.resolve()
    require(not destination.is_relative_to(root) and not root.is_relative_to(destination), 'Use a separate course archive, not the old archive, its parent or a child.')
    with c.lock(root):
        value=inspect(root,proposal_id);data=value['proposal'];asset=validate(root,data)
        require(value['binding']==binding(root) and value['asset_hash']==c.digest(asset), 'Course progress, settings or assets changed; prepare a fresh proposal.')
        continuation={'schema':1,'proposal_hash':value['hash'],'source_course':str(root),'source_binding':value['binding'],'consent':consent}
        if destination.exists():
            p=destination/'continuation.json'
            require(p.is_file() and c.read(p)['proposal_hash']==value['hash'] and c.read(destination/'config.json')==data['config'] and c.read(destination/'plan.json')==data['plan'], 'Destination exists; no existing course or files were changed.')
            return {'project':str(destination),'status':c.read(destination/'state.json')['status'],'proposal_hash':value['hash']}
        destination.parent.mkdir(parents=True,exist_ok=True)
        # Build privately on the same filesystem. Failures leave no partial learner course.
        with tempfile.TemporaryDirectory(prefix='.omni-course-',dir=destination.parent) as temporary:
            staged=Path(temporary)/'course';staged.mkdir(mode=0o700)
            target=staged/data['plan']['figure']['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(asset,target);target.chmod(0o600)
            if data['config'].get('materials'):
                import omni_materials as m
                for selection in data['config']['materials']['selections']:
                    snapshot=m.load(root,selection['id'],selection['version'])
                    m.save(staged,('items',selection['id'],selection['version']+'.json'),snapshot)
            textbook=data['config'].get('textbook')
            if textbook:
                from omni_textbook_fetch import source_pdf
                original=source_pdf(root,textbook['book_id'],textbook['version'])
                archived=staged/original.relative_to(root)
                archived.parent.mkdir(parents=True,mode=0o700,exist_ok=True)
                shutil.copyfile(original,archived)
                archived.chmod(0o600)
                source_pdf(staged,textbook['book_id'],textbook['version'])
            c.initialize(staged,data['config'],data['plan']);c.save(staged/'continuation.json',continuation)
            # Reserve the final directory exclusively; never replace a concurrently created archive.
            destination.mkdir(mode=0o700)
            try:
                for child in staged.iterdir():shutil.move(str(child),destination/child.name)
            except OSError:
                # A partial course is retained for diagnosis, never force-deleted or approved.
                raise RuntimeError('Course creation interrupted; inspect the private destination before retrying.')
    return {'project':str(destination),'status':'awaiting_approval','proposal_hash':value['hash']}
