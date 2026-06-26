#!/usr/bin/env bash
# OpenClaw Memory Stack — Expertise Graph
# Community detection and expertise clustering on top of the knowledge graph.
# Sourced by wrappers; not run standalone.
set -euo pipefail

EXPERTISE_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_ROOT="${OPENCLAW_INSTALL_ROOT:-$HOME/.openclaw/memory-stack}"
source "$INSTALL_ROOT/lib/contracts.sh"

NOWLEDGE_URL="${OPENCLAW_NOWLEDGE_URL:-http://127.0.0.1:14242}"

# ============================================================
# Build expertise graph via Louvain community detection
# ============================================================
build_expertise_graph() {
  local collection="${1:-}"

  if ! has_command python3; then
    echo '{"status": "error", "message": "python3 required for expertise graph"}' >&2
    return 1
  fi

  # 1. Export all nodes and edges from Nowledge graph
  local raw_data="" tmpfile
  tmpfile=$(mktemp)

  local search_url="$NOWLEDGE_URL/api/memories?limit=500"
  curl -sf -o "$tmpfile" "$search_url" 2>/dev/null || true
  raw_data=$(cat "$tmpfile" 2>/dev/null)
  rm -f "$tmpfile"

  if [ -z "$raw_data" ] || [ "$raw_data" = "null" ] || [ "$raw_data" = "[]" ]; then
    echo '{"status": "empty", "message": "No memories found to build expertise graph", "clusters": []}'
    return 0
  fi

  # 2. Run Louvain community detection via networkx
  python3 -c "
import json, sys

raw = '''$(json_escape "$raw_data")'''
collection_filter = '''$collection'''

try:
    data = json.loads(raw) if raw else []
except:
    data = []

if isinstance(data, dict):
    data = data.get('results', data.get('memories', []))

# Build a graph from memories
# Nodes = unique entities/topics mentioned; Edges = co-occurrence in same memory
import re
from collections import defaultdict

def extract_entities(text):
    \"\"\"Extract meaningful tokens from memory content.\"\"\"
    text = str(text).lower()
    # Extract quoted terms, capitalized words, and key phrases
    quoted = re.findall(r'[\"\\']([^\"\\'\n]{2,40})[\"\\']', text)
    # Also grab standalone meaningful words (3+ chars, not stopwords)
    stopwords = {'the','and','for','are','but','not','you','all','can','her','was','one','our',
                 'out','has','had','how','its','may','new','now','old','see','way','who','did',
                 'get','let','say','she','too','use','with','this','that','from','have','been',
                 'will','each','make','like','just','over','such','take','than','them','very',
                 'some','into','most','other','after','also','these','about','which','their',
                 'would','there','could','where','should','what','when','does','more','been'}
    words = re.findall(r'\\b[a-z][a-z0-9_.-]{2,30}\\b', text)
    meaningful = [w for w in words if w not in stopwords]
    # Deduplicate, prefer quoted terms
    seen = set()
    entities = []
    for term in quoted + meaningful[:20]:
        t = term.strip().lower()
        if t and t not in seen and len(t) > 2:
            seen.add(t)
            entities.append(t)
    return entities[:15]

# Build co-occurrence graph
node_set = set()
edges = defaultdict(int)
node_memory_count = defaultdict(int)

for item in data:
    content = item.get('content', item.get('text', str(item)))
    entities = extract_entities(content)
    for e in entities:
        node_set.add(e)
        node_memory_count[e] += 1
    # Create edges between co-occurring entities
    for i, e1 in enumerate(entities):
        for e2 in entities[i+1:]:
            pair = tuple(sorted([e1, e2]))
            edges[pair] += 1

# Filter: keep only nodes with 2+ occurrences for meaningful clusters
significant_nodes = {n for n in node_set if node_memory_count[n] >= 2}
if len(significant_nodes) < 3:
    significant_nodes = node_set  # Fall back to all if too few

# Build graph data structure
graph_data = {
    'nodes': [{'id': n, 'memory_count': node_memory_count[n]} for n in significant_nodes],
    'edges': [{'source': s, 'target': t, 'weight': w}
              for (s, t), w in edges.items()
              if s in significant_nodes and t in significant_nodes]
}

# Try networkx Louvain; fall back to simple connected-component clustering
try:
    import networkx as nx
    from networkx.algorithms.community import louvain_communities

    G = nx.Graph()
    for node in graph_data['nodes']:
        G.add_node(node['id'], memory_count=node['memory_count'])
    for edge in graph_data['edges']:
        G.add_edge(edge['source'], edge['target'], weight=edge.get('weight', 1))

    communities = louvain_communities(G, resolution=1.0)
    pagerank = nx.pagerank(G)

    result = []
    for i, community in enumerate(communities):
        members = [{'id': n, 'pagerank': round(pagerank.get(n, 0), 6),
                     'memory_count': node_memory_count.get(n, 0)} for n in community]
        members.sort(key=lambda x: -x['pagerank'])
        result.append({
            'cluster_id': i,
            'size': len(community),
            'top_nodes': members[:5],
            'all_members': [m['id'] for m in members]
        })

    result.sort(key=lambda x: -x['size'])
    print(json.dumps({
        'status': 'success',
        'total_nodes': len(significant_nodes),
        'total_edges': len(graph_data['edges']),
        'cluster_count': len(result),
        'clusters': result,
        'method': 'louvain'
    }, indent=2))

except ImportError:
    # Fallback: simple connected-component clustering without networkx
    # Union-Find for connected components
    parent = {n['id']: n['id'] for n in graph_data['nodes']}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for edge in graph_data['edges']:
        if edge['source'] in parent and edge['target'] in parent:
            union(edge['source'], edge['target'])

    clusters = defaultdict(list)
    for n in parent:
        clusters[find(n)].append(n)

    result = []
    for i, (root, members) in enumerate(sorted(clusters.items(), key=lambda x: -len(x[1]))):
        member_info = [{'id': m, 'memory_count': node_memory_count.get(m, 0)} for m in members]
        member_info.sort(key=lambda x: -x['memory_count'])
        result.append({
            'cluster_id': i,
            'size': len(members),
            'top_nodes': member_info[:5],
            'all_members': [m['id'] for m in member_info]
        })

    print(json.dumps({
        'status': 'success',
        'total_nodes': len(significant_nodes),
        'total_edges': len(graph_data['edges']),
        'cluster_count': len(result),
        'clusters': result,
        'method': 'connected_components'
    }, indent=2))
" 2>/dev/null
}

# ============================================================
# Query expertise for a specific topic
# ============================================================
query_expertise() {
  local topic="$1"

  if [ -z "$topic" ]; then
    echo '{"status": "error", "message": "topic is required"}' >&2
    return 1
  fi

  if ! has_command python3; then
    echo '{"status": "error", "message": "python3 required"}' >&2
    return 1
  fi

  # First build the expertise graph, then find the matching cluster
  local graph_json
  graph_json=$(build_expertise_graph)

  python3 -c "
import json, sys

topic = '''$topic'''.lower()
graph = json.loads('''$(json_escape "$graph_json")''')

if graph.get('status') != 'success':
    print(json.dumps({'status': 'empty', 'message': 'No expertise graph available', 'topic': topic}))
    sys.exit(0)

# Find clusters containing the topic
matches = []
for cluster in graph.get('clusters', []):
    members = cluster.get('all_members', [])
    # Check if topic matches any member
    for member in members:
        if topic in member or member in topic:
            matches.append({
                'cluster_id': cluster['cluster_id'],
                'cluster_size': cluster['size'],
                'top_nodes': cluster['top_nodes'],
                'match_on': member,
                'all_members': members
            })
            break

if not matches:
    # Partial match: check if topic appears as substring
    for cluster in graph.get('clusters', []):
        for member in cluster.get('all_members', []):
            if any(w in member for w in topic.split()):
                matches.append({
                    'cluster_id': cluster['cluster_id'],
                    'cluster_size': cluster['size'],
                    'top_nodes': cluster['top_nodes'],
                    'match_on': member,
                    'all_members': cluster['all_members']
                })
                break

result = {
    'status': 'success' if matches else 'empty',
    'topic': topic,
    'matching_clusters': matches,
    'total_clusters': graph.get('cluster_count', 0),
    'method': graph.get('method', 'unknown')
}
print(json.dumps(result, indent=2))
" 2>/dev/null
}
