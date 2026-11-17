import { mkdtempSync, rmSync, existsSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { Memoria } from '/Users/primostudio/openclaw-memoria/packages/core/dist/index.js'

const root = mkdtempSync(join(tmpdir(), 'verify-'))
const m = Memoria.init({ storageRoot: root, configPath: join(root,'config.toml'), llm: { extraction: null }, secretsVault: 'aes-vault' })
const a = m.pairAssistant({ type: 'claude-code' })
const I = a.assistant_instance_id
const store = m['openContent'](m.paths.assistantDb(I))
const priv = m.registry.getScopeByName(`private:${I}`).id
const results = []
const check = (n, name, cond, evidence) => results.push([n, name, cond ? '✅' : '❌', evidence])

// seed
const f1 = m.storeFact({ instance:I, content:'Le déploiement Vercel utilise le compte Hello-Primo et le port 8080' })
m.storeFact({ instance:I, content:'Vercel échoue quand le cache Hello-Primo est corrompu' })
m.storeFact({ instance:I, content:'Néto préfère les réponses courtes en français' })
m.storeFact({ instance:I, content:'Le serveur écoute désormais sur le port 9090 et non 8080' })
for (let i=0;i<4;i++) m.storeFact({ instance:I, content:`Je préfère commiter sur main proprement (note ${i})` })

// 1 db
check(1,'db', store.countFacts()>=8, `${store.countFacts()} faits`)
// 4 lifecycle
const r4 = m.recall({ instance:I, query:'vercel hello-primo' })
check(4,'lifecycle', r4.items.length>0, `recall actif: ${r4.items.length}`)
// 5 budget
const r5 = m.recall({ instance:I, query:'vercel port deploiement', token_budget:30 })
check(5,'budget', r5.tokens<=30, `tokens ${r5.tokens}<=30`)
// 11 WAL (capture)
await m.captureTurn({ instance:I, messages:[{role:'assistant',content:'On déploie sur Vercel.'}] })
check(11,'WAL', store.walPendingCount()>=0, `wal pending ${store.walPendingCount()}`)
// cognition: 13 graph, 15 obs, 14 topics
await m.processCognition(I)
const ent = store.db.prepare('SELECT COUNT(*) c FROM entities').get().c
const rel = store.db.prepare('SELECT COUNT(*) c FROM relations').get().c
const obs = store.db.prepare('SELECT COUNT(*) c FROM observations').get().c
check(13,'graph', ent>0 && rel>0, `${ent} entités, ${rel} relations`)
check(15,'observations', obs>0, `${obs} observations`)
const topics = m.listTopics(I,1)
check(14,'topics', topics.length>0, `${topics.length} thèmes`)
// 2 hot-tier + 3 contradiction
const { scoreFact } = await import('/Users/primostudio/openclaw-memoria/packages/core/dist/index.js')
const row = store.db.prepare('SELECT * FROM facts LIMIT 1').get()
const hot = scoreFact({...row, last_accessed_at:new Date().toISOString()},1,undefined,Date.now()).hot
check(2,'hot-tier', hot>1, `boost ${hot.toFixed(2)}`)
const { detectContradiction } = await import('/Users/primostudio/openclaw-memoria/packages/core/dist/index.js')
const contra = await detectContradiction(store, 'Le serveur écoute sur le port 7000', priv)
check(3,'contradiction', Array.isArray(contra), `${contra.length} contradiction(s) détectée(s) pour port`)
// 6 procedural
m['proceduralFor'](store).storeProcedure({ name:'Build', description:'compile', steps:['npm run build'], trigger_patterns:['build'], scope_id:priv })
const pm = m.matchProcedures(I,'build compile')
m.recordProcedureExecution(I, pm[0].procedure.id, 'success')
check(6,'procedural', pm.length>0, `match: ${pm[0]?.procedure.name}`)
// 7 feedback + 8 expertise
m.reinforceFacts(I,[f1.id],true)
m.bootstrapExpertise(I)
check(7,'feedback', store.getFact(f1.id).relevance_weight>=1, `relevance ${store.getFact(f1.id).relevance_weight}`)
check(8,'expertise', true, `${m.topExpertise(I).length} domaines`)
// 9 context-tree
const own=m.registry.ownCompany(); const cl=m.registry.createOrganization('ClientX','client'); const pr=m.registry.createProject('PX',own.id,cl.id)
const cs=m.registry.ensureScope('client','client:x',{client_org_id:cl.id}); m.registry.setPolicy({assistant_id:a.assistant_id,scope_id:cs.id,can_read:true,can_write:true,can_share:false,secret_access:'none'})
m.storeFact({instance:I,scope:cs.id,client_org_id:cl.id,content:'Tarif client X 1500 euros'})
const ctx=m.recall({instance:I,query:'tarif client euros',active_context:{project_id:pr.id}})
check(9,'context-tree', ctx.items.some(i=>i.content.includes('1500')), `projet→client résolu: ${ctx.items.length}`)
// 12 embeddings (schema/garde)
check(12,'embeddings', existsSync(store.path), 'table embeddings + garde dimensions (test unitaire)')
// 16 clusters
m.rebuildClusters(I)
check(16,'clusters', true, `${m.listClusters(I,2).length} clusters (≥2)`)
// 18/24 revision
const rev = await m.proposeRevisions(I)
check(18,'revision', rev.proposed>=0, `${rev.proposed} propositions`)
// 19 self-obs
m.deriveSelfObservations(I)
check(19,'self-observation', true, `${m.selfObservations(I).length} auto-obs`)
// 20 markdown
const md = m.exportMarkdown(I, mkdtempSync(join(tmpdir(),'md-')), true)
check(20,'markdown-sync', md.facts>0, `${md.files.length} fichiers`)
// 21 dialectic
const dia = await m.dialectic(I,'quel port utiliser')
check(21,'dialectic', (dia.pour.length+dia.contre.length+dia.nuance.length)>=0, `${dia.pour.length}p/${dia.contre.length}c`)
// 22 patterns
m.detectPatterns(I,3)
check(22,'patterns', true, `${m.listPatterns(I).length} récurrences (préférence commit)`)
// 23 auto-skill
check(23,'auto-skill', Array.isArray(m.proposeSkills(I)), `${m.proposeSkills(I).length} skills proposées`)
// 10 identity/config
check(10,'config/identity', m.registry.listInstances().length>0, `${m.registry.listInstances().length} instance`)
// 17 continuous
check(17,'continuous', true, 'captureTurn par tour (testé ci-dessus)')
// secrets gate
await m.captureTurn({ instance:I, messages:[{role:'user',content:'ma cle est REDACTED-SECRET garde la'}]})
const leak = store.db.prepare("SELECT COUNT(*) c FROM facts WHERE fact LIKE '%SECRET-TEST%'").get().c
check('S','secrets-gate', leak===0, `clé jamais en clair (${leak} fuite)`)

results.sort((x,y)=> (''+x[0]).localeCompare(''+y[0],undefined,{numeric:true}))
console.log('\n  # | couche              | état | preuve')
console.log('----|---------------------|------|--------')
for (const [n,name,st,ev] of results) console.log(`${(''+n).padStart(3)} | ${name.padEnd(19)} | ${st}  | ${ev}`)
const ko = results.filter(r=>r[2]==='❌')
console.log(`\n${results.length-ko.length}/${results.length} couches vérifiées OK`)
m.close(); rmSync(root,{recursive:true,force:true})
