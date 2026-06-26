"""
Memory System - CLI Interface
"""
import argparse
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from memory_manager import MemoryManager
from shared_memory import SharedMemoryManager


def cmd_add(manager: MemoryManager, args):
    tags = args.tags.split(',') if args.tags else None
    metadata = None
    if args.meta:
        import json
        try:
            metadata = json.loads(args.meta)
        except:
            print("Error: Invalid JSON in --meta")
            return 1
    
    entry = manager.add(
        content=args.content,
        tags=tags,
        metadata=metadata,
        generate_embedding=args.embed,
        group=args.group
    )
    print(f"✓ Memory added: {entry.id}")
    print(f"  Time: {entry.timestamp}")
    if entry.tags:
        print(f"  Tags: {', '.join(entry.tags)}")
    if entry.group:
        print(f"  Group: {entry.group}")
    return 0


def cmd_get(manager: MemoryManager, args):
    entry = manager.get(args.id)
    if entry:
        print(f"ID: {entry.id}")
        print(f"Time: {entry.timestamp}")
        print(f"Tags: {', '.join(entry.tags) if entry.tags else '(none)'}")
        print(f"\nContent:\n{entry.content}")
        if entry.embedding:
            print(f"\n[Has embedding vector: {len(entry.embedding)} dims]")
        if entry.metadata:
            print(f"\nMetadata: {entry.metadata}")
    else:
        print(f"Memory not found: {args.id}")
        return 1
    return 0


def cmd_delete(manager: MemoryManager, args):
    if manager.delete(args.id):
        print(f"✓ Deleted: {args.id}")
        return 0
    else:
        print(f"Failed to delete: {args.id}")
        return 1


def cmd_list(manager: MemoryManager, args):
    tags = args.tags.split(',') if args.tags else None
    total = manager.count(tags=tags)
    
    if total == 0:
        print("No memories found.")
        return 0
    
    # Pagination info
    limit = args.limit or total
    offset = args.offset or 0
    page_info = ""
    if args.limit or args.offset:
        page_info = f" (showing {offset}-{min(offset+limit, total)} of {total})"
    
    entries = manager.list(tags=tags, limit=args.limit, offset=args.offset)
    
    print(f"Total: {total} memories{page_info}\n")
    for e in entries:
        tags_str = f" [{', '.join(e.tags)}]" if e.tags else ""
        preview = e.content[:60] + "..." if len(e.content) > 60 else e.content
        has_embed = "📎" if e.embedding else "  "
        print(f"{has_embed} [{e.id}] {e.timestamp[:10]}{tags_str}")
        print(f"    {preview}")
        print()
    
    # Pagination hint
    if total > (offset + limit):
        remaining = total - (offset + limit)
        print(f"  → {remaining} more memories. Use --offset {offset + limit} to see more")
    
    return 0


def cmd_search(manager: MemoryManager, args):
    tags = args.tags.split(',') if args.tags else None
    results = manager.search(
        query=args.query,
        tags=tags,
        top_k=args.top_k,
        threshold=args.threshold
    )
    
    if not results:
        print("No matching memories found.")
        return 0
    
    print(f"Found {len(results)} matching memories:\n")
    for r in results:
        score = r.get('similarity', 0)
        tags_str = f" [{', '.join(r.get('tags', []))}]" if r.get('tags') else ""
        preview = r['content'][:80] + "..." if len(r['content']) > 80 else r['content']
        print(f"📊 {score:.2%} [{r['id'][:8]}...]{tags_str}")
        print(f"   {preview}")
        print()
    return 0


def cmd_export(manager: MemoryManager, args):
    if args.output:
        manager.export_json(args.output)
        print(f"✓ Exported to: {args.output}")
    else:
        print(manager.export_json())
    return 0


def cmd_import(manager: MemoryManager, args):
    count = manager.import_json(filepath=args.file)
    print(f"✓ Imported {count} memories from: {args.file}")
    return 0


def cmd_batch_delete(manager: MemoryManager, args):
    """Delete multiple memories"""
    ids = [i.strip() for i in args.ids.split(',')]
    
    if not args.force:
        print(f"⚠️  About to delete {len(ids)} memories:")
        for id in ids:
            entry = manager.get(id)
            if entry:
                print(f"  - {id[:12]}... : {entry.content[:40]}...")
            else:
                print(f"  - {id[:12]}... : (not found)")
        print(f"\nType 'yes' to confirm: ", end='')
        confirm = input()
        if confirm.lower() != 'yes':
            print("Cancelled.")
            return 0
    
    result = manager.batch_delete(ids)
    print(f"✓ Deleted {result['deleted']} memories")
    if result['failed']:
        print(f"⚠️  Failed to delete {result['failed']}: {result['failed_ids']}")
    
    return 0


def cmd_batch_add_tags(manager: MemoryManager, args):
    """Add tags to multiple memories"""
    ids = [i.strip() for i in args.ids.split(',')]
    tags = [t.strip() for t in args.tags.split(',')]
    
    result = manager.batch_add_tags(ids, tags)
    print(f"✓ Updated {result['updated']} memories")
    if result['failed']:
        print(f"⚠️  Failed to update {result['failed']}: {result['failed_ids']}")
    
    return 0


def cmd_batch_remove_tags(manager: MemoryManager, args):
    """Remove tags from multiple memories"""
    ids = [i.strip() for i in args.ids.split(',')]
    tags = [t.strip() for t in args.tags.split(',')]
    
    result = manager.batch_remove_tags(ids, tags)
    print(f"✓ Updated {result['updated']} memories")
    if result['failed']:
        print(f"⚠️  Failed to update {result['failed']}: {result['failed_ids']}")
    
    return 0


# ============= Group Commands =============

def cmd_group_list(manager: MemoryManager, args):
    """List all groups"""
    groups = manager.list_groups()
    
    if not groups:
        print("No groups found.")
        return 0
    
    print(f"📁 Groups ({len(groups)}):\n")
    for group in groups:
        count = len(manager.get_by_group(group))
        print(f"  {group}: {count} memories")
    
    return 0


def cmd_group_show(manager: MemoryManager, args):
    """Show memories in a group"""
    entries = manager.get_by_group(args.group)
    
    if not entries:
        print(f"No memories in group '{args.group}'")
        return 0
    
    print(f"📁 Group '{args.group}' ({len(entries)} memories):\n")
    for e in entries:
        tags_str = f" [{', '.join(e.tags)}]" if e.tags else ""
        preview = e.content[:60] + "..." if len(e.content) > 60 else e.content
        print(f"  [{e.id[:12]}...] {e.timestamp[:10]}{tags_str}")
        print(f"      {preview}")
    
    return 0


def cmd_group_add(manager: MemoryManager, args):
    """Add memories to a group"""
    ids = [i.strip() for i in args.ids.split(',')]
    
    result = manager.add_to_group(ids, args.group)
    print(f"✓ Added {result['updated']} memories to group '{args.group}'")
    if result['failed']:
        print(f"⚠️  Failed: {result['failed_ids']}")
    
    return 0


def cmd_group_remove(manager: MemoryManager, args):
    """Remove memories from a group"""
    ids = [i.strip() for i in args.ids.split(',')]
    
    result = manager.remove_from_group(ids)
    print(f"✓ Removed {result['updated']} memories from group")
    if result['failed']:
        print(f"⚠️  Failed: {result['failed_ids']}")
    
    return 0


def cmd_group_delete(manager: MemoryManager, args):
    """Delete a group"""
    if args.delete_memories:
        confirm = input(f"⚠️  This will DELETE all memories in group '{args.group}'. Type 'yes' to confirm: ")
        if confirm.lower() != 'yes':
            print("Cancelled.")
            return 0
        result = manager.delete_group(args.group, delete_memories=True)
        print(f"✓ Deleted group and {result['deleted_memories']} memories")
    else:
        result = manager.delete_group(args.group)
        print(f"✓ Removed all memories from group '{args.group}'")
    
    return 0


def cmd_rebuild_embeds(manager: MemoryManager, args):
    count = manager.rebuild_all_embeddings()
    print(f"✓ Rebuilt embeddings for {count} memories")
    return 0


def cmd_update_embed(manager: MemoryManager, args):
    entry = manager.update_embedding(args.id)
    if entry:
        print(f"✓ Updated embedding for: {entry.id}")
    else:
        print(f"Memory not found: {args.id}")
        return 1
    return 0


# ============= Shared Memory Commands =============

def cmd_shared_add(shared_mgr: SharedMemoryManager, args):
    """Add a shared memory"""
    tags = args.tags.split(',') if args.tags else None
    
    entry = shared_mgr.add(
        content=args.content,
        agent_id=args.agent,
        tags=tags
    )
    print(f"✓ Shared memory added: {entry.id}")
    print(f"  Shared by: {args.agent}")
    print(f"  Time: {entry.timestamp}")
    if entry.tags:
        print(f"  Tags: {', '.join(entry.tags)}")
    return 0


def cmd_shared_list(shared_mgr: SharedMemoryManager, args):
    """List shared memories"""
    tags = args.tags.split(',') if args.tags else None
    agent_filter = args.agent
    
    if agent_filter:
        entries = shared_mgr.get_by_agent(agent_filter)
    else:
        entries = shared_mgr.list(tags=tags)
    
    if not entries:
        print("No shared memories found.")
        return 0
    
    print(f"Total: {len(entries)} shared memories\n")
    for e in entries:
        tags_str = f" [{', '.join(e.tags)}]" if e.tags else ""
        preview = e.content[:60] + "..." if len(e.content) > 60 else e.content
        has_embed = "📎" if e.embedding else "  "
        shared_by = e.metadata.get('shared_by', 'unknown') if e.metadata else 'unknown'
        print(f"{has_embed} [{e.id[:8]}] {e.timestamp[:10]} by {shared_by}{tags_str}")
        print(f"    {preview}")
        print()
    return 0


def cmd_shared_search(shared_mgr: SharedMemoryManager, args):
    """Search shared memories"""
    tags = args.tags.split(',') if args.tags else None
    
    results = shared_mgr.search(
        query=args.query,
        tags=tags,
        top_k=args.top_k,
        threshold=args.threshold
    )
    
    if not results:
        print("No matching shared memories found.")
        return 0
    
    print(f"Found {len(results)} matching shared memories:\n")
    for r in results:
        score = r.get('similarity', 0)
        tags_str = f" [{', '.join(r.get('tags', []))}]" if r.get('tags') else ""
        preview = r['content'][:80] + "..." if len(r['content']) > 80 else r['content']
        shared_by = r.get('metadata', {}).get('shared_by', 'unknown')
        print(f"📊 {score:.2%} [{r['id'][:8]}] by {shared_by}{tags_str}")
        print(f"   {preview}")
        print()
    return 0


def cmd_shared_get(shared_mgr: SharedMemoryManager, args):
    """Get a shared memory by ID"""
    entry = shared_mgr.get(args.id)
    if entry:
        shared_by = entry.metadata.get('shared_by', 'unknown') if entry.metadata else 'unknown'
        print(f"ID: {entry.id}")
        print(f"Shared by: {shared_by}")
        print(f"Time: {entry.timestamp}")
        print(f"Tags: {', '.join(entry.tags) if entry.tags else '(none)'}")
        print(f"\nContent:\n{entry.content}")
        if entry.embedding:
            print(f"\n[Has embedding vector: {len(entry.embedding)} dims]")
        if entry.metadata:
            print(f"\nMetadata: {entry.metadata}")
    else:
        print(f"Shared memory not found: {args.id}")
        return 1
    return 0


def cmd_shared_delete(shared_mgr: SharedMemoryManager, args):
    """Delete a shared memory"""
    if shared_mgr.delete(args.id):
        print(f"✓ Deleted shared memory: {args.id}")
        return 0
    else:
        print(f"Failed to delete: {args.id}")
        return 1


# ============= Summarize Commands =============

def cmd_summarize(manager: MemoryManager, args):
    """Summarize conversation and optionally save to memory"""
    from summarizer import MemorySummarizer, ConversationMemoryProcessor
    
    # Read conversation from file or direct input
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            conversation = f.read()
    elif args.conversation:
        conversation = args.conversation
    else:
        print("Error: Provide either --file or --conversation")
        return 1
    
    # Initialize summarizer (auto-detects OpenClaw model)
    summarizer = MemorySummarizer(
        llm_provider=args.provider,
        model=args.model,
        base_url=args.base_url
    )
    
    print(f"Using model: {summarizer.model} ({summarizer.llm_provider})")
    
    processor = ConversationMemoryProcessor(
        memory_manager=manager,
        summarizer=summarizer,
        auto_save=args.save
    )
    
    results = processor.process(
        conversation=conversation,
        context=args.context,
        tags=args.tags.split(',') if args.tags else None
    )
    
    if not results:
        print("No memories generated.")
        return 0
    
    print(f"📝 Generated {len(results)} memory entries:\n")
    for i, entry in enumerate(results, 1):
        tags_str = f" [{', '.join(entry.tags)}]" if entry.tags else ""
        print(f"{i}. {entry.content}")
        print(f"   Type: {entry.metadata.get('memory_type', 'unknown')}{tags_str}")
        print()
    
    if args.save:
        print(f"✓ {len(results)} memories saved to memory store")
    
    return 0


# ============= Template Commands =============

def cmd_template_list(manager: MemoryManager, args):
    """List all available templates"""
    from templates import MemoryTemplates
    
    templates = MemoryTemplates.list_all()
    
    print(f"📋 Available templates ({len(templates)}):\n")
    for name, tmpl in templates.items():
        print(f"  {name}")
        print(f"    {tmpl.description}")
        print(f"    Tags: {', '.join(tmpl.default_tags)}")
        print()
    
    print("Use 'memory template show <name>' to see template details")
    return 0


def cmd_template_show(manager: MemoryManager, args):
    """Show template details"""
    from templates import MemoryTemplates
    
    guide = MemoryTemplates.render_template_cli(args.template)
    
    if not guide:
        print(f"Template not found: {args.template}")
        print(f"Use 'memory template list' to see available templates")
        return 1
    
    print(guide)
    return 0


def cmd_template_use(manager: MemoryManager, args):
    """Create memory from template"""
    from templates import MemoryTemplates
    
    template = MemoryTemplates.get_template(args.template)
    if not template:
        print(f"Template not found: {args.template}")
        return 1
    
    # Parse field values from --field arguments
    field_values = {}
    if args.field:
        for f in args.field:
            if '=' not in f:
                print(f"Invalid field format: {f}. Use field_name=value")
                return 1
            key, value = f.split('=', 1)
            field_values[key] = value
    
    if not field_values:
        print("Error: --field required. Example: --field title='My task' --field priority='高'")
        print(f"\nTemplate fields for '{args.template}':")
        guide = MemoryTemplates.render_template_cli(args.template)
        print(guide)
        return 1
    
    result = MemoryTemplates.generate_from_template(args.template, field_values)
    
    if not result:
        print("Failed to generate from template")
        return 1
    
    # Add the memory
    entry = manager.add(
        content=result['content'],
        tags=args.tags.split(',') if args.tags else result['tags']
    )
    
    print(f"✓ Memory created from template '{args.template}': {entry.id}")
    print(f"\nContent:\n{result['content']}")
    
    return 0


# ============= Maintenance Commands =============

def cmd_maintenance_review(manager: MemoryManager, args):
    """Review old memories"""
    from maintenance import MemoryMaintenance
    
    maint = MemoryMaintenance(manager)
    
    result = maint.run_review(
        older_than_days=args.days,
        max_memories=args.max
    )
    
    if result["status"] == "no_old_memories":
        print(result["message"])
        return 0
    
    print(f"📋 Reviewed {result['reviewed']} of {result['total_old']} old memories (> {result['cutoff_days']} days)\n")
    
    for r in result["results"]:
        print(f"ID: {r['id'][:12]}...")
        print(f"Content: {r['content'][:60]}...")
        if r["issues"]:
            print(f"⚠️  Issues: {', '.join(r['issues'])}")
        if r["suggestions"]:
            print(f"💡 Suggestions: {', '.join(r['suggestions'])}")
        print()
    
    return 0


def cmd_maintenance_tagsuggest(manager: MemoryManager, args):
    """Suggest tags for untagged memories"""
    from maintenance import MemoryMaintenance
    
    maint = MemoryMaintenance(manager)
    
    result = maint.suggest_tags_for_memories(
        limit=args.limit,
        use_llm=not args.no_llm
    )
    
    if result["status"] == "no_untagged":
        print("✓ All memories already have tags")
        return 0
    
    print(f"📋 Suggested tags for {result['count']} untagged memories")
    if result["remaining_untagged"] > 0:
        print(f"  ({result['remaining_untagged']} more untagged)\n")
    
    for item in result["suggestions"]:
        print(f"ID: {item['id'][:12]}...")
        print(f"  Content: {item['content_preview']}...")
        print(f"  Suggested: {', '.join(item['suggested_tags'])}")
        print(f"  → Use 'python3 memory add \"...\" --tags \"{','.join(item['suggested_tags'])}\"' to add")
        print()
    
    return 0


def cmd_maintenance_consolidate(manager: MemoryManager, args):
    """Find similar memories - requires user confirmation to delete"""
    from maintenance import MemoryMaintenance
    
    maint = MemoryMaintenance(manager)
    
    result = maint.consolidate_similar(threshold=args.threshold)
    
    if result["status"] == "insufficient_memories":
        print(result["message"])
        return 0
    
    if result["status"] == "no_similar_found":
        print("✓ No similar memories found")
        return 0
    
    print(f"📋 Found {len(result['pairs'])} similar memory pairs\n")
    print("⚠️  Manual review required - use 'memory delete <id>' to remove duplicates\n")
    
    for i, pair in enumerate(result["pairs"], 1):
        print(f"Pair {i} ({pair['similarity']:.0%} similar):")
        print(f"  Keep: [{pair['keep_id'][:12]}...] {pair['keep_content']}")
        print(f"  Drop: [{pair['drop_id'][:12]}...] {pair['drop_content']}")
        print()
    
    print("To delete a duplicate, run:")
    print(f"  python3 memory delete <id>")
    
    return 0


def cmd_maintenance_expand(manager: MemoryManager, args):
    """Expand a short memory"""
    from maintenance import MemoryMaintenance
    
    maint = MemoryMaintenance(manager)
    
    entry = maint.expand_summary(args.id, args.context)
    
    if entry:
        print(f"✓ Expanded memory {args.id[:12]}...")
        print(f"\nNew content:\n{entry.content}")
    else:
        print(f"Memory not found: {args.id}")
        return 1
    
    return 0


def cmd_maintenance_outdated(manager: MemoryManager, args):
    """Manage outdated memories - flag for user review"""
    from maintenance import MemoryMaintenance
    
    maint = MemoryMaintenance(manager)
    
    if args.list:
        outdated = maint.list_outdated()
        if not outdated:
            print("No outdated memories")
            return 0
        
        print(f"📋 {len(outdated)} outdated memories:\n")
        for m in outdated:
            reason = m.metadata.get('outdated_reason', 'No reason')
            print(f"  [{m.id[:12]}...] {m.content[:50]}...")
            print(f"    Reason: {reason}")
            print(f"    → Use 'memory delete {m.id}' to remove")
            print()
        return 0
    
    elif args.mark:
        entry = maint.mark_outdated(args.mark, args.reason)
        if entry:
            print(f"✓ Marked as outdated: {args.mark[:12]}...")
            print(f"  → Use 'memory delete {args.mark}' to remove")
        else:
            print(f"Memory not found: {args.mark}")
            return 1
        return 0
    
    elif args.unmark:
        entry = maint.unmark_outdated(args.unmark)
        if entry:
            print(f"✓ Unmarked: {args.unmark[:12]}...")
        else:
            print(f"Memory not found: {args.unmark}")
            return 1
        return 0
    
    print("Use --list, --mark <id>, or --unmark <id>")
    return 0


def cmd_maintenance_report(manager: MemoryManager, args):
    """Generate maintenance report"""
    from maintenance import MemoryMaintenance
    
    maint = MemoryMaintenance(manager)
    print(maint.generate_report())
    return 0


def main():
    parser = argparse.ArgumentParser(description="Memory System CLI")
    parser.add_argument(
        '--config', '-c',
        help='Path to config.yaml',
        default=None
    )
    parser.add_argument(
        '--backend', '-b',
        choices=['local', 'github', 'gitee', 'sqlite'],
        help='Storage backend (overrides config)',
        default=None
    )
    parser.add_argument(
        '--embedding', '-e',
        action='store_true',
        help='Enable embedding model',
        default=None
    )
    parser.add_argument(
        '--no-embedding',
        action='store_true',
        help='Disable embedding model',
        default=None
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # add
    p_add = subparsers.add_parser('add', help='Add a new memory')
    p_add.add_argument('content', help='Memory content')
    p_add.add_argument('--tags', '-t', help='Comma-separated tags')
    p_add.add_argument('--meta', '-m', help='JSON metadata')
    p_add.add_argument('--embed', action='store_true', help='Generate embedding')
    p_add.add_argument('--group', '-g', help='Group name')
    
    # get
    p_get = subparsers.add_parser('get', help='Get a memory by ID')
    p_get.add_argument('id', help='Memory ID')
    
    # delete
    p_del = subparsers.add_parser('delete', help='Delete a memory')
    p_del.add_argument('id', help='Memory ID')
    
    # list
    p_list = subparsers.add_parser('list', help='List all memories')
    p_list.add_argument('--tags', help='Filter by comma-separated tags')
    p_list.add_argument('--limit', '-l', type=int, help='Maximum number to show')
    p_list.add_argument('--offset', '-o', type=int, default=0, help='Skip first N entries')
    
    # search
    p_search = subparsers.add_parser('search', help='Search memories')
    p_search.add_argument('query', help='Search query')
    p_search.add_argument('--tags', help='Filter by comma-separated tags')
    p_search.add_argument('--top-k', type=int, default=5, help='Number of results')
    p_search.add_argument('--threshold', type=float, default=0.7, help='Similarity threshold')
    
    # export
    p_exp = subparsers.add_parser('export', help='Export all memories')
    p_exp.add_argument('--output', '-o', help='Output file path')
    
    # import
    p_imp = subparsers.add_parser('import', help='Import memories from JSON')
    p_imp.add_argument('file', help='JSON file to import')
    
    # batch-delete
    p_batch_delete = subparsers.add_parser('batch-delete', help='Delete multiple memories')
    p_batch_delete.add_argument('ids', help='Comma-separated memory IDs')
    p_batch_delete.add_argument('--force', '-f', action='store_true', help='Skip confirmation')
    
    # batch-add-tags
    p_batch_add_tags = subparsers.add_parser('batch-add-tags', help='Add tags to multiple memories')
    p_batch_add_tags.add_argument('ids', help='Comma-separated memory IDs')
    p_batch_add_tags.add_argument('--tags', '-t', required=True, help='Comma-separated tags')
    
    # batch-remove-tags
    p_batch_remove_tags = subparsers.add_parser('batch-remove-tags', help='Remove tags from multiple memories')
    p_batch_remove_tags.add_argument('ids', help='Comma-separated memory IDs')
    p_batch_remove_tags.add_argument('--tags', '-t', required=True, help='Comma-separated tags')
    
    # ========== Group Subcommands ==========
    p_group = subparsers.add_parser('group', help='Memory group commands')
    group_subparsers = p_group.add_subparsers(dest='group_command', help='Group subcommands')
    
    # group list
    p_group_list = group_subparsers.add_parser('list', help='List all groups')
    
    # group show
    p_group_show = group_subparsers.add_parser('show', help='Show memories in a group')
    p_group_show.add_argument('group', help='Group name')
    
    # group add
    p_group_add = group_subparsers.add_parser('add', help='Add memories to a group')
    p_group_add.add_argument('group', help='Group name')
    p_group_add.add_argument('ids', help='Comma-separated memory IDs')
    
    # group remove
    p_group_remove = group_subparsers.add_parser('remove', help='Remove memories from a group')
    p_group_remove.add_argument('ids', help='Comma-separated memory IDs')
    
    # group delete
    p_group_delete = group_subparsers.add_parser('delete', help='Delete a group')
    p_group_delete.add_argument('group', help='Group name')
    p_group_delete.add_argument('--delete-memories', action='store_true', help='Also delete memories in group')
    
    # rebuild-embeds
    p_rebuild = subparsers.add_parser('rebuild-embeds', help='Rebuild all embeddings')
    
    # update-embed
    p_upd = subparsers.add_parser('update-embed', help='Update embedding for one memory')
    p_upd.add_argument('id', help='Memory ID')
    
    # ========== Shared Memory Subcommands ==========
    p_shared = subparsers.add_parser('shared', help='Shared memory commands')
    shared_subparsers = p_shared.add_subparsers(dest='shared_command', help='Shared memory subcommands')
    
    # shared add
    p_shared_add = shared_subparsers.add_parser('add', help='Add a shared memory')
    p_shared_add.add_argument('content', help='Shared memory content')
    p_shared_add.add_argument('--agent', '-a', default='default', help='Agent ID sharing this memory')
    p_shared_add.add_argument('--tags', '-t', help='Comma-separated tags')
    
    # shared list
    p_shared_list = shared_subparsers.add_parser('list', help='List shared memories')
    p_shared_list.add_argument('--tags', help='Filter by comma-separated tags')
    p_shared_list.add_argument('--agent', '-a', help='Filter by agent ID')
    
    # shared search
    p_shared_search = shared_subparsers.add_parser('search', help='Search shared memories')
    p_shared_search.add_argument('query', help='Search query')
    p_shared_search.add_argument('--tags', help='Filter by comma-separated tags')
    p_shared_search.add_argument('--top-k', type=int, default=5, help='Number of results')
    p_shared_search.add_argument('--threshold', type=float, default=0.7, help='Similarity threshold')
    
    # shared get
    p_shared_get = shared_subparsers.add_parser('get', help='Get a shared memory by ID')
    p_shared_get.add_argument('id', help='Memory ID')
    
    # shared delete
    p_shared_del = shared_subparsers.add_parser('delete', help='Delete a shared memory')
    p_shared_del.add_argument('id', help='Memory ID')
    
    # Add shared-backend argument to all shared subcommands
    for p in [p_shared_add, p_shared_list, p_shared_search, p_shared_get, p_shared_del]:
        p.add_argument(
            '--shared-backend', '-sb',
            choices=['local', 'github', 'gitee', 'sqlite'],
            help='Shared memory storage backend',
            default=None
        )
        p.add_argument(
            '--shared-path',
            help='Shared memory path/repo',
            default=None
        )
    
    # ========== Summarize Subcommand ==========
    p_summarize = subparsers.add_parser('summarize', help='Summarize conversation into memories')
    p_summarize.add_argument('--conversation', help='Conversation text to summarize')
    p_summarize.add_argument('--file', '-f', help='File containing conversation text')
    p_summarize.add_argument('--context', help='Additional context about the conversation')
    p_summarize.add_argument('--tags', '-t', help='Additional tags for generated memories')
    p_summarize.add_argument('--save', '-s', action='store_true', help='Save generated memories to store')
    p_summarize.add_argument('--provider', choices=['openai', 'anthropic', 'ollama'], help='LLM provider')
    p_summarize.add_argument('--model', '-m', help='LLM model name')
    p_summarize.add_argument('--base-url', help='API base URL (for custom endpoints)')
    
    # ========== Template Subcommand ==========
    p_template = subparsers.add_parser('template', help='Memory template commands')
    template_subparsers = p_template.add_subparsers(dest='template_command', help='Template subcommands')
    
    # template list
    p_template_list = template_subparsers.add_parser('list', help='List all templates')
    
    # template show
    p_template_show = template_subparsers.add_parser('show', help='Show template details')
    p_template_show.add_argument('template', help='Template name')
    
    # template use
    p_template_use = template_subparsers.add_parser('use', help='Create memory from template')
    p_template_use.add_argument('template', help='Template name')
    p_template_use.add_argument('--field', '-f', action='append', help='Field values (name=value)')
    p_template_use.add_argument('--tags', '-t', help='Override default tags')
    
    # ========== Maintenance Subcommand ==========
    p_maint = subparsers.add_parser('maintenance', help='Memory maintenance commands')
    maint_subparsers = p_maint.add_subparsers(dest='maint_command', help='Maintenance subcommands')
    
    # maintenance review
    p_maint_review = maint_subparsers.add_parser('review', help='Review old memories')
    p_maint_review.add_argument('--days', type=int, default=7, help='Review memories older than N days')
    p_maint_review.add_argument('--max', type=int, default=10, help='Maximum memories to review')
    
    # maintenance consolidate
    p_maint_consol = maint_subparsers.add_parser('consolidate', help='Merge similar memories')
    p_maint_consol.add_argument('--threshold', type=float, default=0.85, help='Similarity threshold (0-1)')
    p_maint_consol.add_argument('--apply', action='store_true', help='Apply changes (default is dry-run)')
    
    # maintenance expand
    p_maint_expand = maint_subparsers.add_parser('expand', help='Expand a short memory')
    p_maint_expand.add_argument('id', help='Memory ID to expand')
    p_maint_expand.add_argument('--context', help='Additional context for expansion')
    
    # maintenance outdated
    p_maint_outdated = maint_subparsers.add_parser('outdated', help='Manage outdated memories')
    p_maint_outdated.add_argument('--list', '-l', action='store_true', help='List outdated memories')
    p_maint_outdated.add_argument('--mark', help='Mark a memory as outdated')
    p_maint_outdated.add_argument('--unmark', help='Remove outdated mark')
    p_maint_outdated.add_argument('--reason', '-r', help='Reason for marking outdated')
    
    # maintenance report
    p_maint_report = maint_subparsers.add_parser('report', help='Generate maintenance report')
    
    # maintenance suggest-tags
    p_maint_tags = maint_subparsers.add_parser('suggest-tags', help='Suggest tags for untagged memories')
    p_maint_tags.add_argument('--limit', '-l', type=int, default=10, help='Max memories to process')
    p_maint_tags.add_argument('--no-llm', action='store_true', help='Use keyword-based instead of LLM')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Determine embedding setting
    use_embedding = None
    if args.embedding:
        use_embedding = True
    elif args.no_embedding:
        use_embedding = False
    
    # Handle shared memory commands
    if args.command == 'shared':
        if not args.shared_command:
            p_shared.print_help()
            return 0
        
        # Determine shared memory settings
        shared_backend = args.shared_backend or 'local'
        shared_path = args.shared_path or './shared_memory'
        
        # Initialize shared memory manager
        try:
            shared_mgr = SharedMemoryManager(
                backend=shared_backend,
                shared_path=shared_path,
                use_embedding=use_embedding or False
            )
        except Exception as e:
            print(f"Error initializing shared memory manager: {e}")
            return 1
        
        shared_commands = {
            'add': cmd_shared_add,
            'list': cmd_shared_list,
            'search': cmd_shared_search,
            'get': cmd_shared_get,
            'delete': cmd_shared_delete,
        }
        
        return shared_commands[args.shared_command](shared_mgr, args)
    
    try:
        manager = MemoryManager(
            config_path=args.config,
            backend=args.backend,
            use_embedding=use_embedding
        )
    except Exception as e:
        print(f"Error initializing memory manager: {e}")
        return 1
    
    # Command handlers
    commands = {
        'add': cmd_add,
        'get': cmd_get,
        'delete': cmd_delete,
        'list': cmd_list,
        'search': cmd_search,
        'export': cmd_export,
        'import': cmd_import,
        'batch-delete': cmd_batch_delete,
        'batch-add-tags': cmd_batch_add_tags,
        'batch-remove-tags': cmd_batch_remove_tags,
        'group': cmd_group_list,  # Will be overridden by subparser
        'rebuild-embeds': cmd_rebuild_embeds,
        'update-embed': cmd_update_embed,
        'summarize': cmd_summarize,
    }
    
    # Handle group commands
    if args.command == 'group':
        if not args.group_command:
            p_group.print_help()
            return 0
        
        group_commands = {
            'list': cmd_group_list,
            'show': cmd_group_show,
            'add': cmd_group_add,
            'remove': cmd_group_remove,
            'delete': cmd_group_delete,
        }
        
        return group_commands[args.group_command](manager, args)
    
    # Handle template commands
    if args.command == 'template':
        if not args.template_command:
            p_template.print_help()
            return 0
        
        template_commands = {
            'list': cmd_template_list,
            'show': cmd_template_show,
            'use': cmd_template_use,
        }
        
        return template_commands[args.template_command](manager, args)
    
    # Handle maintenance commands
    if args.command == 'maintenance':
        if not args.maint_command:
            p_maint.print_help()
            return 0
        
        maint_commands = {
            'review': cmd_maintenance_review,
            'consolidate': cmd_maintenance_consolidate,
            'expand': cmd_maintenance_expand,
            'outdated': cmd_maintenance_outdated,
            'report': cmd_maintenance_report,
            'suggest-tags': cmd_maintenance_tagsuggest,
        }
        
        return maint_commands[args.maint_command](manager, args)
    
    return commands[args.command](manager, args)


if __name__ == '__main__':
    sys.exit(main())
