#!/usr/bin/env python3
"""MindGardener CLI — a hippocampus for AI agents."""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from . import __version__
from .config import load_config
from .recall import recall, list_entities


def cmd_init(args):
    """Initialize a new MindGardener workspace."""
    workspace = Path(args.path or ".").resolve()
    
    print(f"🌱 Initializing MindGardener workspace at {workspace}")
    
    # Create directories
    (workspace / "memory" / "entities").mkdir(parents=True, exist_ok=True)
    print(f"  ✅ Created memory/entities/")
    
    # Create config
    config_path = workspace / "garden.yaml"
    if not config_path.exists():
        config_path.write_text(f"""# MindGardener configuration
workspace: {workspace}
memory_dir: memory/
entities_dir: memory/entities/
graph_file: memory/graph.jsonl
long_term_memory: MEMORY.md

extraction:
  provider: google        # google, openai, anthropic, ollama, compatible
  model: gemini-2.0-flash
  temperature: 0.1

consolidation:
  surprise_threshold: 0.5
  decay_days: 30
""")
        print(f"  ✅ Created garden.yaml")
    else:
        print(f"  ⏭️  garden.yaml already exists")
    
    # Create MEMORY.md
    memory_path = workspace / "MEMORY.md"
    if not memory_path.exists():
        memory_path.write_text("# Long-term Memory\n\n")
        print(f"  ✅ Created MEMORY.md")
    
    # Create today's daily file
    from datetime import date
    today = date.today().isoformat()
    daily_path = workspace / "memory" / f"{today}.md"
    if not daily_path.exists():
        daily_path.write_text(f"# {today}\n\n## Notes\n\n")
        print(f"  ✅ Created memory/{today}.md")
    
    print(f"\n🌱 Ready! Next steps:")
    print(f"  1. Set your LLM key: export GEMINI_API_KEY=your-key")
    print(f"  2. Write notes in memory/{today}.md")
    print(f"  3. Run: garden extract")
    print(f"  4. Query: garden recall \"topic\"")


def cmd_extract(args):
    """Extract entities from daily log files."""
    from .core import process_date
    cfg = load_config(args.config)
    
    if args.all:
        import glob
        files = sorted(cfg.memory_dir.glob("2*-*-*.md"))
        import re
        for f in files:
            if re.match(r'^\d{4}-\d{2}-\d{2}$', f.stem):
                process_date(f.stem)
    elif args.date:
        process_date(args.date)
    else:
        process_date(date.today().isoformat())


def cmd_surprise(args):
    """Run surprise scoring with two-stage prediction error."""
    cfg = load_config(args.config)
    date_str = args.date or date.today().isoformat()
    
    if args.legacy:
        # Use simple single-prompt scoring
        from .core import run_surprise
        run_surprise(date_str)
    else:
        # Use two-stage prediction error engine
        from .prediction_error import PredictionErrorEngine
        from .providers import get_provider
        
        llm = get_provider(cfg.extraction.provider, model=cfg.extraction.model)
        engine = PredictionErrorEngine(llm, cfg.memory_dir, cfg.long_term_memory)
        result = engine.compute_sync(date_str)
        
        print(f"\n🧠 Prediction Error Report — {date_str}")
        print(f"   Mean PE: {result.mean_surprise:.2f}")
        print(f"   Predictions made: {len(result.predictions)}")
        print(f"   Events scored: {len(result.errors)}")
        
        if result.high_surprise:
            print(f"\n🔴 High surprise ({len(result.high_surprise)}):")
            for e in result.high_surprise:
                print(f"   [{e.prediction_error:.2f}] {e.event}")
                print(f"         → {e.reason}")
        
        if result.medium_surprise:
            print(f"\n🟡 Medium surprise ({len(result.medium_surprise)}):")
            for e in result.medium_surprise:
                print(f"   [{e.prediction_error:.2f}] {e.event}")
        
        if result.model_updates:
            print(f"\n📝 Suggested world model updates:")
            for u in result.model_updates:
                print(f"   - {u}")


def cmd_consolidate(args):
    """Run full sleep cycle: PE scoring → MEMORY.md update."""
    cfg = load_config(args.config)
    date_str = args.date or date.today().isoformat()
    
    if args.legacy:
        from .core import run_consolidate
        run_consolidate()
    else:
        from .consolidator import Consolidator
        from .providers import get_provider
        
        llm = get_provider(cfg.extraction.provider, model=cfg.extraction.model)
        consolidator = Consolidator(llm, cfg.memory_dir, cfg.long_term_memory)
        result = consolidator.run_sync(date_str)
        print(result)


def cmd_recall(args):
    """Query the knowledge graph."""
    cfg = load_config(args.config)
    result = recall(args.query, cfg, hops=args.hops)
    print(result)


def cmd_entities(args):
    """List all known entities."""
    cfg = load_config(args.config)
    entities = list_entities(cfg)
    
    if args.json:
        print(json.dumps(entities, indent=2))
    else:
        # Group by type
        by_type: dict[str, list] = {}
        for e in entities:
            by_type.setdefault(e["type"], []).append(e)
        
        for entity_type, items in sorted(by_type.items()):
            print(f"\n{entity_type.upper()} ({len(items)})")
            for item in items:
                entries = item["timeline_entries"]
                print(f"  {item['name']} ({entries} entries)")


def cmd_prune(args):
    """Archive stale entities, show what's going cold."""
    cfg = load_config(args.config)
    from .decay import DecayConfig, run_decay
    
    dc = DecayConfig(archive_after_days=args.days)
    actions = run_decay(
        cfg.entities_dir,
        graph_file=cfg.graph_file,
        config=dc,
        dry_run=args.dry_run
    )
    for action in actions:
        print(action)


def cmd_merge(args):
    """Merge duplicate entities or detect potential duplicates."""
    cfg = load_config(args.config)
    from .aliases import merge_entities, detect_duplicates
    
    if args.detect:
        dupes = detect_duplicates(cfg.entities_dir)
        if dupes:
            print("🔍 Potential duplicates:")
            for a, b, conf in dupes:
                print(f"  [{conf:.0%}] {a} ↔ {b}")
            print(f"\nMerge with: garden merge \"source\" \"target\"")
        else:
            print("No duplicates detected.")
    elif args.source and args.target:
        merge_entities(cfg.entities_dir, args.source, args.target)
    else:
        print("Usage: garden merge \"source\" \"target\"")
        print("       garden merge --detect")


def cmd_context(args):
    """Assemble token-budget-aware context for a query."""
    cfg = load_config(args.config)
    from .context import assemble_context
    
    result = assemble_context(
        query=args.query,
        config=cfg,
        token_budget=args.budget,
        include_recent_days=args.days,
        max_entities=args.max_entities,
    )
    
    manifest = result["manifest"]
    
    if args.manifest_only:
        import json
        print(json.dumps(manifest, indent=2))
    else:
        print(result["context"])
        print(f"\n--- Manifest ---")
        print(f"Tokens: {manifest['tokens_used']}/{manifest['token_budget']} ({manifest['utilization']:.0%})")
        print(f"Loaded: {manifest['loaded_count']} sources")
        if manifest['skipped']:
            print(f"Skipped: {manifest['skipped_count']} sources")
            for s in manifest['skipped']:
                print(f"  - {s['type']}: {s.get('name', s.get('date', '?'))} ({s['reason']})")


def cmd_fix(args):
    """Correct entity data without re-running extraction."""
    cfg = load_config(args.config)
    from .fix import fix_type, fix_name, add_fact, remove_fact
    
    actions = {
        "type": lambda: fix_type(cfg.entities_dir, args.entity, args.value),
        "name": lambda: fix_name(cfg.entities_dir, args.entity, args.value),
        "add-fact": lambda: add_fact(cfg.entities_dir, args.entity, args.value),
        "rm-fact": lambda: remove_fact(cfg.entities_dir, args.entity, args.value),
    }
    result = actions[args.action]()
    print(result)


def cmd_reindex(args):
    """Rebuild graph.jsonl from entity files after manual edits."""
    cfg = load_config(args.config)
    from .reindex import reindex
    
    print("🔄 Reindexing graph from entity files...")
    stats = reindex(cfg)
    
    print(f"  📄 Scanned {stats['entities']} entities")
    print(f"  🔗 Found {stats['triplets']} relationships")
    if cfg.graph_file.with_suffix(".jsonl.bak").exists():
        print(f"  💾 Old graph backed up to graph.jsonl.bak")
    print("✅ Graph rebuilt.")


def cmd_viz(args):
    """Visualize the knowledge graph as Mermaid."""
    cfg = load_config(args.config)
    
    if not cfg.graph_file.exists():
        print("No graph data yet. Run 'garden extract' first.")
        return
    
    seen = set()
    print("graph LR")
    for line in cfg.graph_file.read_text().strip().split("\n"):
        if not line:
            continue
        try:
            t = json.loads(line)
            s = t["subject"].replace(" ", "_").replace("#", "Nr").replace(".", "")
            o = t["object"].replace(" ", "_").replace("#", "Nr").replace(".", "")
            p = t["predicate"]
            key = f"{s}-{p}-{o}"
            if key not in seen:
                seen.add(key)
                print(f"    {s} -->|{p}| {o}")
        except:
            continue


def cmd_evaluate(args):
    """Evaluate agent output against the knowledge graph."""
    cfg = load_config(args.config)
    from .evaluate import evaluate_output, write_back

    text = args.text
    if args.file:
        text = Path(args.file).read_text()
    if not text:
        print("❌ Provide text with --text or --file")
        return

    result = evaluate_output(text, cfg)
    print(result.summary())

    if args.write_back:
        actions = write_back(result, cfg, min_confidence=args.min_confidence, dry_run=args.dry_run)
        if actions:
            print(f"\n### Write-back Actions")
            for a in actions:
                print(f"  {a}")

    if args.json:
        print(json.dumps(result.to_json(), indent=2))


def cmd_beliefs(args):
    """View and manage the self-model (identity-level beliefs)."""
    cfg = load_config(args.config)
    model_path = cfg.memory_dir / "self-model.yaml"

    if args.bootstrap:
        # Bootstrap from MEMORY.md or provided text
        from .self_model import SelfModelEngine
        from .providers import get_provider

        source = cfg.long_term_memory
        if not source.exists():
            print("❌ No MEMORY.md found. Write one first, or use --input.")
            return

        text = source.read_text()
        # Also include recent entities for richer bootstrapping
        entity_texts = []
        if cfg.entities_dir.exists():
            for f in sorted(cfg.entities_dir.glob("*.md"))[:20]:
                entity_texts.append(f.read_text()[:500])
        if entity_texts:
            text += "\n\n## Entity Context\n" + "\n".join(entity_texts)

        llm = get_provider(cfg.extraction.provider, model=cfg.extraction.model)
        engine = SelfModelEngine(llm, model_path)

        print("🧠 Bootstrapping self-model from MEMORY.md + entities...")
        model = engine.bootstrap_sync(text)
        print(f"✅ Created {len(model.beliefs)} beliefs in memory/self-model.yaml\n")
        print(model.format_readable())

    elif args.drift:
        # Detect drift from today's events
        from .self_model import SelfModelEngine
        from .providers import get_provider

        date_str = args.date or date.today().isoformat()
        daily_path = cfg.memory_dir / f"{date_str}.md"

        if not daily_path.exists():
            print(f"❌ No daily log for {date_str}")
            return
        if not model_path.exists():
            print("❌ No self-model yet. Run: garden beliefs --bootstrap")
            return

        llm = get_provider(cfg.extraction.provider, model=cfg.extraction.model)
        engine = SelfModelEngine(llm, model_path)

        events = daily_path.read_text()
        print(f"🔍 Detecting identity drift from {date_str}...")
        drifts = engine.detect_drift_sync(events)
        print(engine.format_drifts(drifts))

        if drifts and args.apply:
            model = engine.apply_drifts(drifts, significance_threshold=args.threshold)
            print(f"\n✅ Applied {len([d for d in drifts if d.significance >= args.threshold])} drifts to self-model.")

    else:
        # Show current beliefs
        from .self_model import SelfModel

        if not model_path.exists():
            print("No self-model yet. Bootstrap with: garden beliefs --bootstrap")
            return

        model = SelfModel.from_yaml(model_path.read_text())

        if args.json:
            print(json.dumps([b.to_dict() for b in model.active_beliefs()], indent=2))
        elif args.weak:
            weak = model.weakening()
            if weak:
                print("⚠ Weakening Beliefs:")
                for b in weak:
                    print(f"  [{b.confidence:.0%}] {b.claim}")
                    if b.evidence_against:
                        print(f"       Counter: {', '.join(b.evidence_against[-3:])}")
            else:
                print("No weakening beliefs.")
        else:
            print(model.format_readable())


def cmd_add(args):
    """Add a fact manually with provenance tracking."""
    from .core import append_to_graph, MEMORY_DIR
    from datetime import date, datetime
    import os
    
    cfg = load_config(args.config)
    
    # Parse fact into triplet
    fact = args.fact
    
    # Build triplet
    triplet = {
        "subject": args.subject or "Marcus",  # Default subject
        "predicate": args.predicate or "noted",
        "object": fact,
        "detail": args.detail or "",
    }
    
    # Build provenance
    provenance = {
        "source": args.source or "manual",
        "agent": args.agent or os.environ.get("AGENT_ID", "user"),
        "confidence": args.confidence or 0.9,
    }
    
    date_str = args.date or date.today().isoformat()
    
    # Add to graph
    append_to_graph([triplet], date_str, provenance=provenance)
    
    print(f"✅ Added fact with provenance:")
    print(f"   {triplet['subject']} → {triplet['predicate']} → {triplet['object']}")
    print(f"   Source: {provenance['source']}")
    print(f"   Agent: {provenance['agent']}")
    print(f"   Confidence: {provenance['confidence']}")
    
    # Optionally add topics
    if args.topics:
        topics = [t.strip() for t in args.topics.split(",")]
        print(f"   Topics: {', '.join(topics)}")


def cmd_sync(args):
    """Sync agent memories to shared memory."""
    from .sync import sync_all_agents, sync_agent_to_shared, list_agents
    cfg = load_config(args.config)
    
    if args.list:
        agents = list_agents(cfg.workspace)
        print(f"🔄 Registered agents: {len(agents)}")
        for a in agents:
            print(f"  - {a}")
        return
    
    if args.agent:
        print(f"🔄 Syncing {args.agent} to shared memory...")
        result = sync_agent_to_shared(
            cfg.workspace,
            args.agent,
            dry_run=not args.apply,
        )
    else:
        print("🔄 Syncing all agents to shared memory...")
        result = sync_all_agents(
            cfg.workspace,
            dry_run=not args.apply,
        )
    
    print(f"  Added: {result.get('total_added', result.get('added', 0))}")
    print(f"  Conflicts: {result.get('total_conflicts', result.get('conflicts', 0))}")
    
    if not args.apply:
        print("  (dry run - use --apply to merge)")


def cmd_decay(args):
    """Show decay scores and optionally prune old facts."""
    from .decay import apply_decay_to_graph, prune_decayed
    cfg = load_config(args.config)
    
    if args.prune:
        kept, pruned = prune_decayed(
            cfg.graph_file,
            threshold=args.threshold,
            half_life_days=args.half_life,
            dry_run=args.dry_run,
        )
        action = "Would prune" if args.dry_run else "Pruned"
        print(f"⏰ Decay Pruning")
        print(f"  {action}: {pruned} facts below {args.threshold} threshold")
        print(f"  Keeping: {kept} facts")
        if args.dry_run:
            print(f"  (use --apply to actually prune)")
    else:
        # Just show scores
        scored = apply_decay_to_graph(cfg.graph_file, args.half_life)
        
        print(f"⏰ Decay Scores (half-life: {args.half_life} days)")
        print(f"  Total facts: {len(scored)}")
        
        # Show lowest scoring
        low = [f for f in scored if f.get("_decay_score", 1) < 0.5]
        if low:
            print(f"\n  Decaying ({len(low)} below 50%):")
            for f in low[:10]:
                score = f.get("_decay_score", 0)
                subj = f.get("subject", "?")
                pred = f.get("predicate", "?")
                obj = f.get("object", "?")[:30]
                print(f"    [{score:.1%}] {subj} → {pred} → {obj}")


def cmd_inject(args):
    """Generate context for session injection."""
    from .inject import generate_context, write_recall_context
    cfg = load_config(args.config)
    
    if args.output:
        # Write to file
        output_path = Path(args.output)
        write_recall_context(
            cfg,
            output_path=output_path,
            query=args.query,
            max_tokens=args.budget,
            strategy=args.strategy,
        )
        print(f"✅ Wrote context to {output_path}")
    else:
        # Print to stdout
        context = generate_context(
            cfg,
            query=args.query,
            max_tokens=args.budget,
            strategy=args.strategy,
        )
        print(context)


def cmd_conflicts(args):
    """List and manage detected conflicts."""
    cfg = load_config(args.config)
    conflicts_file = cfg.memory_dir / "conflicts.md"
    
    if not conflicts_file.exists():
        print("No conflicts detected yet.")
        return
    
    content = conflicts_file.read_text()
    
    # Count conflicts
    unresolved = content.count("**Status:** Unresolved")
    resolved = content.count("**Status:** Resolved")
    
    print(f"⚠️ Conflicts Summary")
    print(f"  Unresolved: {unresolved}")
    print(f"  Resolved:   {resolved}")
    print(f"  Total:      {unresolved + resolved}")
    
    if args.show:
        print(f"\n--- conflicts.md ---\n")
        print(content)
    
    if args.clear_resolved:
        # Remove resolved conflicts from file
        lines = content.split("\n## ")
        header = lines[0]
        conflicts = lines[1:] if len(lines) > 1 else []
        
        unresolved_conflicts = [c for c in conflicts if "**Status:** Unresolved" in c]
        
        new_content = header + "\n## ".join([""] + unresolved_conflicts) if unresolved_conflicts else header
        conflicts_file.write_text(new_content.strip() + "\n")
        print(f"  Cleared {resolved} resolved conflicts.")


def cmd_stats(args):
    """Show garden statistics."""
    cfg = load_config(args.config)
    
    entities = list_entities(cfg)
    
    # Count triplets
    triplet_count = 0
    if cfg.graph_file.exists():
        triplet_count = sum(1 for line in cfg.graph_file.read_text().strip().split("\n") if line)
    
    # Count surprises
    surprise_count = 0
    if cfg.surprise_file.exists():
        surprise_count = sum(1 for line in cfg.surprise_file.read_text().strip().split("\n") if line)
    
    # Count daily files
    import re
    daily_count = sum(1 for f in cfg.memory_dir.glob("*.md") 
                      if re.match(r'^\d{4}-\d{2}-\d{2}$', f.stem))
    
    print(f"🌱 MindGardener Stats")
    print(f"  Entities:      {len(entities)}")
    print(f"  Triplets:      {triplet_count}")
    print(f"  Surprises:     {surprise_count}")
    print(f"  Daily files:   {daily_count}")
    print(f"  Workspace:     {cfg.workspace}")
    
    if entities:
        types = {}
        for e in entities:
            types[e["type"]] = types.get(e["type"], 0) + 1
        print(f"\n  Entity types:")
        for t, c in sorted(types.items(), key=lambda x: -x[1]):
            print(f"    {t}: {c}")


def main():
    parser = argparse.ArgumentParser(
        prog="garden",
        description="🌱 MindGardener — A hippocampus for AI agents",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--config", "-c", help="Path to garden.yaml config file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress non-essential output")
    
    sub = parser.add_subparsers(dest="command", help="Available commands")
    
    # init
    p_init = sub.add_parser("init", help="Initialize a new MindGardener workspace")
    p_init.add_argument("path", nargs="?", help="Workspace path (default: current dir)")
    p_init.set_defaults(func=cmd_init)
    
    # extract
    p_extract = sub.add_parser("extract", help="Extract entities from daily logs")
    p_extract.add_argument("--date", "-d", help="Specific date (YYYY-MM-DD)")
    p_extract.add_argument("--all", action="store_true", help="Process all daily files")
    p_extract.set_defaults(func=cmd_extract)
    
    # surprise
    p_surprise = sub.add_parser("surprise", help="Run two-stage prediction error scoring")
    p_surprise.add_argument("--date", "-d", help="Date to score (default: today)")
    p_surprise.add_argument("--legacy", action="store_true", help="Use simple single-prompt scoring")
    p_surprise.set_defaults(func=cmd_surprise)
    
    # consolidate
    p_consolidate = sub.add_parser("consolidate", help="Run sleep cycle: PE → MEMORY.md")
    p_consolidate.add_argument("--date", "-d", help="Date to consolidate (default: today)")
    p_consolidate.add_argument("--legacy", action="store_true", help="Use simple consolidation")
    p_consolidate.set_defaults(func=cmd_consolidate)
    
    # recall
    p_recall = sub.add_parser("recall", help="Query the knowledge graph")
    p_recall.add_argument("query", help="What to look up")
    p_recall.add_argument("--hops", type=int, default=1, help="Graph traversal depth")
    p_recall.set_defaults(func=cmd_recall)
    
    # entities
    p_entities = sub.add_parser("entities", help="List all known entities")
    p_entities.add_argument("--json", action="store_true", help="Output as JSON")
    p_entities.set_defaults(func=cmd_entities)
    
    # decay
    p_decay = sub.add_parser("prune", help="Prune stale entities, reinforce active ones")
    p_decay.add_argument("--dry-run", action="store_true", help="Show what would be archived")
    p_decay.add_argument("--days", type=int, default=30, help="Archive after N days inactive")
    p_decay.set_defaults(func=cmd_prune)
    
    # merge
    p_merge = sub.add_parser("merge", help="Merge duplicate entities")
    p_merge.add_argument("source", nargs="?", help="Source entity to merge FROM")
    p_merge.add_argument("target", nargs="?", help="Target entity to merge INTO")
    p_merge.add_argument("--detect", action="store_true", help="Auto-detect potential duplicates")
    p_merge.set_defaults(func=cmd_merge)
    
    # context
    p_ctx = sub.add_parser("context", help="Assemble token-budget-aware context for a query")
    p_ctx.add_argument("query", help="What context to assemble")
    p_ctx.add_argument("--budget", type=int, default=4000, help="Token budget (default: 4000)")
    p_ctx.add_argument("--days", type=int, default=2, help="Recent daily logs to include (default: 2)")
    p_ctx.add_argument("--max-entities", type=int, default=10, help="Max entities to load (default: 10)")
    p_ctx.add_argument("--manifest-only", action="store_true", help="Only show manifest, not context")
    p_ctx.set_defaults(func=cmd_context)
    
    # fix
    p_fix = sub.add_parser("fix", help="Correct entity data without re-extracting")
    p_fix.add_argument("action", choices=["type", "name", "add-fact", "rm-fact"],
                       help="What to fix")
    p_fix.add_argument("entity", help="Entity name")
    p_fix.add_argument("value", help="New value (type/name/fact text)")
    p_fix.set_defaults(func=cmd_fix)
    
    # reindex
    p_reindex = sub.add_parser("reindex", help="Rebuild graph from entity files (after manual edits)")
    p_reindex.set_defaults(func=cmd_reindex)
    
    # viz
    p_viz = sub.add_parser("viz", help="Visualize knowledge graph (Mermaid)")
    p_viz.set_defaults(func=cmd_viz)
    
    # evaluate
    p_eval = sub.add_parser("evaluate", help="Fact-check agent output against knowledge graph")
    p_eval.add_argument("--text", "-t", help="Text to evaluate")
    p_eval.add_argument("--file", "-f", help="File containing text to evaluate")
    p_eval.add_argument("--write-back", "-w", action="store_true", help="Write verified facts back to entities")
    p_eval.add_argument("--dry-run", action="store_true", help="Show what would be written without writing")
    p_eval.add_argument("--min-confidence", type=float, default=0.6, help="Min confidence for write-back (default: 0.6)")
    p_eval.add_argument("--json", action="store_true", help="Output as JSON")
    p_eval.set_defaults(func=cmd_evaluate)

    # beliefs
    p_beliefs = sub.add_parser("beliefs", help="View/manage identity-level self-model")
    p_beliefs.add_argument("--bootstrap", action="store_true", help="Bootstrap self-model from MEMORY.md")
    p_beliefs.add_argument("--drift", action="store_true", help="Detect identity drift from today's events")
    p_beliefs.add_argument("--apply", action="store_true", help="Apply detected drifts to self-model")
    p_beliefs.add_argument("--date", "-d", help="Date for drift detection (default: today)")
    p_beliefs.add_argument("--threshold", type=float, default=0.3, help="Min significance to apply (default: 0.3)")
    p_beliefs.add_argument("--json", action="store_true", help="Output as JSON")
    p_beliefs.add_argument("--weak", action="store_true", help="Show only weakening beliefs")
    p_beliefs.set_defaults(func=cmd_beliefs)
    
    # add (manual fact with provenance)
    p_add = sub.add_parser("add", help="Add a fact manually with provenance tracking")
    p_add.add_argument("fact", help="The fact to add")
    p_add.add_argument("--subject", "-s", help="Subject entity (default: Marcus)")
    p_add.add_argument("--predicate", "-p", help="Relationship verb (default: noted)")
    p_add.add_argument("--detail", help="Additional context")
    p_add.add_argument("--source", help="Source (e.g., 'twitter:@anthropic', 'file:doc.md', 'url:https://...')")
    p_add.add_argument("--agent", help="Agent that recorded this (default: from AGENT_ID env)")
    p_add.add_argument("--confidence", type=float, help="Confidence 0.0-1.0 (default: 0.9)")
    p_add.add_argument("--date", "-d", help="Date (default: today)")
    p_add.add_argument("--topics", help="Comma-separated topics for context-aware injection")
    p_add.set_defaults(func=cmd_add)
    
    # sync
    p_sync = sub.add_parser("sync", help="Sync agent memories to shared memory")
    p_sync.add_argument("--agent", "-a", help="Sync specific agent")
    p_sync.add_argument("--list", action="store_true", help="List registered agents")
    p_sync.add_argument("--apply", action="store_true", help="Actually merge (default: dry run)")
    p_sync.set_defaults(func=cmd_sync)
    
    
    # decay
    p_decay = sub.add_parser("decay", help="Show decay scores and optionally prune")
    p_decay.add_argument("--half-life", type=float, default=30, help="Half-life in days (default: 30)")
    p_decay.add_argument("--threshold", type=float, default=0.1, help="Prune threshold (default: 0.1)")
    p_decay.add_argument("--prune", action="store_true", help="Prune facts below threshold")
    p_decay.add_argument("--dry-run", action="store_true", default=True, help="Don't actually delete (default)")
    p_decay.add_argument("--apply", dest="dry_run", action="store_false", help="Actually prune facts")
    p_decay.set_defaults(func=cmd_decay)
    
    # inject
    p_inject = sub.add_parser("inject", help="Generate context for session injection")
    p_inject.add_argument("--query", "-q", help="Focus context on specific topic")
    p_inject.add_argument("--output", "-o", help="Write to file (default: stdout)")
    p_inject.add_argument("--budget", type=int, default=2000, help="Token budget (default: 2000)")
    p_inject.add_argument("--strategy", choices=["recent_only", "recent_and_relevant", "query_based"],
                         default="recent_and_relevant", help="Injection strategy")
    p_inject.set_defaults(func=cmd_inject)
    
    # conflicts
    p_conflicts = sub.add_parser("conflicts", help="List and manage detected conflicts")
    p_conflicts.add_argument("--show", action="store_true", help="Show full conflicts.md")
    p_conflicts.add_argument("--clear-resolved", action="store_true", help="Remove resolved conflicts from file")
    p_conflicts.set_defaults(func=cmd_conflicts)

    # stats
    p_stats = sub.add_parser("stats", help="Show garden statistics")
    p_stats.set_defaults(func=cmd_stats)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
