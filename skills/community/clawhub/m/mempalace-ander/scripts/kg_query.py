#!/usr/bin/env python3
"""
MemPalace Knowledge Graph Query - Consultar el knowledge graph
"""
import sys
import os
import json
import argparse

# Añadir mempalace al path
sys.path.insert(0, '/root/.openclaw/workspace/mempalace')

from mempalace.knowledge_graph import KnowledgeGraph


def main():
    parser = argparse.ArgumentParser(description='Query MemPalace Knowledge Graph')
    parser.add_argument('--entity', help='Entity to query')
    parser.add_argument('--direction', choices=['both', 'incoming', 'outgoing'], default='both',
                        help='Query direction (default: both)')
    parser.add_argument('--as-of', help='Date filter YYYY-MM-DD')
    parser.add_argument('--timeline', action='store_true', help='Get timeline for entity')
    parser.add_argument('--stats', action='store_true', help='Get KG stats')
    
    args = parser.parse_args()
    
    if not args.stats and not args.entity:
        parser.error('--entity is required unless using --stats')
    
    try:
        kg = KnowledgeGraph()
        
        if args.stats:
            result = kg.stats()
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return
        
        if args.timeline:
            result = kg.timeline(args.entity)
            print(json.dumps({
                "entity": args.entity,
                "timeline": result,
                "count": len(result)
            }, indent=2, ensure_ascii=False))
            return
        
        results = kg.query_entity(
            entity=args.entity,
            as_of=args.as_of,
            direction=args.direction
        )
        print(json.dumps({
            "entity": args.entity,
            "as_of": args.as_of,
            "direction": args.direction,
            "facts": results,
            "count": len(results)
        }, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
