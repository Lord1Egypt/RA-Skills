# Graph Path Reasoning - Design Patterns & Algorithms

Comprehensive collection of algorithms, patterns, and implementation strategies for path finding and analysis in knowledge graphs.

## Path Finding Algorithms

### Pattern 1: Breadth-First Search (BFS) for Shortest Path

Find the shortest path (minimum hops) between two nodes using level-by-level traversal.

**Use Case:** Finding most direct connections, quick path discovery

**Implementation:**
```python
def find_shortest_path_bfs(graph, source, target):
    """
    Find shortest path using BFS.
    
    Args:
        graph: Graph structure with adjacency lists
        source: Starting node
        target: Target node
    
    Returns:
        List representing path, or None if no path exists
    """
    from collections import deque
    
    if source == target:
        return [source]
    
    visited = {source}
    queue = deque([(source, [source])])
    
    while queue:
        current, path = queue.popleft()
        
        for neighbor in graph.get(current, []):
            if neighbor == target:
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None  # No path found


# Example:
path = find_shortest_path_bfs(graph, "Alice", "California")
# Returns: ["Alice", "Diana", "TechCorp", "California"]
```

**Complexity:** O(V + E) time, O(V) space  
**Best For:** Shortest connections, explainability

---

### Pattern 2: Dijkstra's Algorithm for Weighted Paths

Find shortest path considering edge weights (confidence, cost, strength).

**Use Case:** Highest confidence paths, cost-optimized routes

**Implementation:**
```python
def find_best_path_dijkstra(graph, source, target, weight_key='confidence'):
    """
    Find path with best weights using Dijkstra's algorithm.
    
    Args:
        graph: Graph with weighted edges
        source: Starting node
        target: Target node
        weight_key: Edge property to optimize (higher is better)
    
    Returns:
        Tuple of (path, total_weight)
    """
    import heapq
    
    # Initialize distances (use negative for maximization)
    distances = {node: float('-inf') for node in graph.nodes()}
    distances[source] = 1.0
    previous = {node: None for node in graph.nodes()}
    
    # Priority queue: (-weight, node)
    pq = [(-1.0, source)]
    visited = set()
    
    while pq:
        neg_weight, current = heapq.heappop(pq)
        current_weight = -neg_weight
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == target:
            # Reconstruct path
            path = []
            node = target
            while node is not None:
                path.append(node)
                node = previous[node]
            return path[::-1], current_weight
        
        # Explore neighbors
        for neighbor, edge_data in graph.get_edges(current):
            edge_weight = edge_data.get(weight_key, 0.5)
            new_weight = current_weight * edge_weight
            
            if new_weight > distances[neighbor]:
                distances[neighbor] = new_weight
                previous[neighbor] = current
                heapq.heappush(pq, (-new_weight, neighbor))
    
    return None, 0  # No path found


# Example:
path, confidence = find_best_path_dijkstra(graph, "Alice", "Bob", 'confidence')
# Returns: (["Alice", "Diana", "TechCorp", "StartupAI", "Frank"], 0.529)
```

**Complexity:** O((V + E) log V)  
**Best For:** Weighted paths, confidence optimization

---

### Pattern 3: Depth-First Search (DFS) for All Paths

Explore all possible paths between two nodes, useful for finding alternatives.

**Use Case:** Finding all connection routes, diversity analysis

**Implementation:**
```python
def find_all_paths_dfs(graph, source, target, max_length=None):
    """
    Find all paths between source and target using DFS.
    
    Args:
        graph: Graph structure
        source: Starting node
        target: Target node
        max_length: Maximum path length (None = unlimited)
    
    Returns:
        List of all paths found
    """
    paths = []
    visited = set()
    
    def dfs(current, target, path):
        if current == target:
            paths.append(path[:])
            return
        
        if max_length and len(path) >= max_length:
            return
        
        for neighbor in graph.get(current, []):
            if neighbor not in path:  # Avoid cycles
                path.append(neighbor)
                dfs(neighbor, target, path)
                path.pop()
    
    dfs(source, target, [source])
    return paths


# Example:
all_paths = find_all_paths_dfs(graph, "Alice", "TechCorp", max_length=5)
# Returns: [
#   ["Alice", "Diana", "TechCorp"],
#   ["Alice", "Bob", "Charlie", "TechCorp"],
#   ["Alice", "Bob", "Diana", "TechCorp"]
# ]
```

**Complexity:** O(V * paths) - exponential in worst case  
**Best For:** Complete path enumeration, small graphs

---

### Pattern 4: K-Shortest Paths

Find top-K paths ranked by relevance (distance, confidence, or composite).

**Use Case:** Multiple recommendations, robustness analysis

**Implementation:**
```python
def find_k_shortest_paths(graph, source, target, k=3, ranking='distance'):
    """
    Find K shortest paths using modified Dijkstra.
    
    Args:
        graph: Graph structure
        source: Starting node
        target: Target node
        k: Number of paths to return
        ranking: 'distance' (hops), 'confidence', or 'composite'
    
    Returns:
        List of K best paths with scores
    """
    import heapq
    
    # Priority queue: (score, node, path, weight)
    pq = []
    results = []
    
    # Initial path
    heapq.heappush(pq, (0, source, [source], 1.0))
    
    while pq and len(results) < k:
        score, current, path, weight = heapq.heappop(pq)
        
        if current == target:
            results.append({
                'path': path,
                'distance': len(path) - 1,
                'confidence': weight,
                'score': score
            })
            continue
        
        # Explore neighbors
        for neighbor, edge_data in graph.get_edges(current):
            if neighbor not in path:  # Avoid cycles
                edge_conf = edge_data.get('confidence', 0.5)
                new_weight = weight * edge_conf
                new_path = path + [neighbor]
                
                # Calculate score
                if ranking == 'distance':
                    new_score = len(new_path)
                elif ranking == 'confidence':
                    new_score = -new_weight  # Negative for min-heap
                else:  # composite
                    dist_score = len(new_path)
                    conf_score = -new_weight
                    new_score = 0.6 * dist_score + 0.4 * conf_score
                
                heapq.heappush(pq, (new_score, neighbor, new_path, new_weight))
    
    return results


# Example:
top_3 = find_k_shortest_paths(graph, "Alice", "Bob", k=3, ranking='composite')
```

**Complexity:** O(K * E log V)  
**Best For:** Multiple alternatives, robustness

---

## Path Ranking Patterns

### Pattern 5: Distance-Based Ranking

Prioritize paths by number of hops (shorter = better).

**Use Case:** Most direct explanations

**Implementation:**
```python
def rank_paths_by_distance(paths):
    """Rank paths by distance (ascending)."""
    return sorted(paths, key=lambda p: len(p['path']) - 1)


# Example:
ranked = rank_paths_by_distance(all_paths)
# First path: shortest distance
```

---

### Pattern 6: Confidence-Based Ranking

Score paths by cumulative relationship confidence.

**Use Case:** Most certain connections

**Implementation:**
```python
def rank_paths_by_confidence(graph, paths):
    """
    Rank paths by cumulative confidence.
    
    Args:
        graph: Graph with edge confidences
        paths: List of paths
    
    Returns:
        Ranked paths with confidence scores
    """
    scored_paths = []
    
    for path in paths:
        confidence = 1.0
        
        # Multiply confidence along path
        for i in range(len(path) - 1):
            edge = graph.get_edge(path[i], path[i + 1])
            edge_conf = edge.get('confidence', 0.5)
            confidence *= edge_conf
        
        scored_paths.append({
            'path': path,
            'confidence': confidence,
            'distance': len(path) - 1
        })
    
    return sorted(scored_paths, key=lambda p: p['confidence'], reverse=True)


# Example:
ranked = rank_paths_by_confidence(graph, all_paths)
# First path: highest confidence
```

---

### Pattern 7: Composite Multi-Criteria Ranking

Combine distance, confidence, and other factors.

**Use Case:** Balanced ranking

**Implementation:**
```python
def rank_paths_composite(graph, paths, weights=None):
    """
    Rank paths using weighted criteria combination.
    
    Args:
        weights: Dict of {criterion: weight}
    """
    if weights is None:
        weights = {'distance': 0.3, 'confidence': 0.5, 'diversity': 0.2}
    
    scored = []
    
    for idx, path in enumerate(paths):
        # Calculate individual scores
        dist_score = 1.0 / len(path)  # Inverse of distance
        
        conf_score = 1.0
        for i in range(len(path) - 1):
            edge = graph.get_edge(path[i], path[i + 1])
            conf_score *= edge.get('confidence', 0.5)
        
        # Diversity (unique edges compared to other paths)
        unique_edges = set()
        for i in range(len(path) - 1):
            unique_edges.add((path[i], path[i + 1]))
        
        div_score = len(unique_edges) / (len(path) - 1 or 1)
        
        # Composite
        composite = (
            weights.get('distance', 0) * dist_score +
            weights.get('confidence', 0) * conf_score +
            weights.get('diversity', 0) * div_score
        )
        
        scored.append({
            'path': path,
            'score': composite,
            'breakdown': {
                'distance': dist_score,
                'confidence': conf_score,
                'diversity': div_score
            }
        })
    
    return sorted(scored, key=lambda p: p['score'], reverse=True)


# Example:
ranked = rank_paths_composite(graph, paths, weights={'distance': 0.4, 'confidence': 0.6})
```

---

## Path Filtering Patterns

### Pattern 8: Relationship Type Filtering

Filter paths to only include specific relationship types.

**Use Case:** Domain-specific path finding (business only, social only, etc.)

**Implementation:**
```python
def filter_paths_by_types(graph, paths, include_types=None, exclude_types=None):
    """
    Filter paths based on relationship types.
    
    Args:
        include_types: Only include these types
        exclude_types: Exclude these types
    
    Returns:
        Filtered paths
    """
    filtered = []
    
    for path in paths:
        valid = True
        
        for i in range(len(path) - 1):
            edge = graph.get_edge(path[i], path[i + 1])
            rel_type = edge.get('type', 'unknown')
            
            if include_types and rel_type not in include_types:
                valid = False
                break
            
            if exclude_types and rel_type in exclude_types:
                valid = False
                break
        
        if valid:
            filtered.append(path)
    
    return filtered


# Example:
business_paths = filter_paths_by_types(
    graph, 
    paths, 
    include_types=['works_at', 'partner_of', 'owns']
)
```

---

### Pattern 9: Confidence Threshold Filtering

Keep only paths with cumulative confidence above threshold.

**Use Case:** Excluding uncertain connections

**Implementation:**
```python
def filter_paths_by_confidence(graph, paths, min_confidence=0.5):
    """
    Filter paths by minimum cumulative confidence.
    
    Args:
        min_confidence: Minimum acceptable confidence (0.0 to 1.0)
    
    Returns:
        Paths meeting threshold
    """
    filtered = []
    
    for path in paths:
        confidence = 1.0
        for i in range(len(path) - 1):
            edge = graph.get_edge(path[i], path[i + 1])
            confidence *= edge.get('confidence', 0.5)
        
        if confidence >= min_confidence:
            filtered.append({
                'path': path,
                'confidence': confidence
            })
    
    return sorted(filtered, key=lambda p: p['confidence'], reverse=True)


# Example:
high_conf = filter_paths_by_confidence(graph, paths, min_confidence=0.7)
```

---

### Pattern 10: Depth Limiting

Restrict maximum path length.

**Use Case:** Controlling complexity, focusing on nearby connections

**Implementation:**
```python
def limit_path_depth(paths, max_depth):
    """Keep only paths with distance <= max_depth."""
    return [p for p in paths if len(p) - 1 <= max_depth]


# Example:
nearby = limit_path_depth(paths, max_depth=3)  # Max 3 hops
```

---

## Path Analysis Patterns

### Pattern 11: Path Diversity Analysis

Measure how many independent paths exist between nodes.

**Use Case:** Network robustness, redundancy analysis

**Implementation:**
```python
def analyze_path_diversity(paths):
    """
    Analyze diversity of paths.
    
    Returns:
        Metrics about path diversity and criticality
    """
    if not paths:
        return {'diversity': 0, 'critical_edges': []}
    
    # Count edge usage
    edge_counts = {}
    for path in paths:
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            edge_counts[edge] = edge_counts.get(edge, 0) + 1
    
    # Find critical edges (in all paths)
    total_paths = len(paths)
    critical_edges = [e for e, count in edge_counts.items() if count == total_paths]
    
    # Diversity score
    unique_edges = len(edge_counts)
    max_possible = total_paths * (len(paths[0]) - 1) if paths else 0
    diversity = unique_edges / max_possible if max_possible else 0
    
    return {
        'total_paths': total_paths,
        'unique_edges': unique_edges,
        'diversity_score': diversity,
        'critical_edges': critical_edges,
        'redundancy': 'HIGH' if diversity > 0.7 else 'MEDIUM' if diversity > 0.4 else 'LOW'
    }


# Example:
diversity = analyze_path_diversity(all_paths)
# Returns: {'total_paths': 5, 'diversity_score': 0.82, 'redundancy': 'HIGH'}
```

---

### Pattern 12: Path Pattern Detection

Identify repeating patterns in paths.

**Use Case:** Understanding common connection structures

**Implementation:**
```python
def detect_path_patterns(graph, paths):
    """
    Identify common patterns in paths.
    
    Returns:
        List of (pattern, frequency, percentage)
    """
    patterns = {}
    
    for path in paths:
        # Extract pattern (node types only)
        node_types = [graph.get_node_type(n) for n in path]
        pattern = ' → '.join(node_types)
        
        patterns[pattern] = patterns.get(pattern, 0) + 1
    
    # Sort by frequency
    sorted_patterns = sorted(
        patterns.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    return [
        {
            'pattern': p,
            'frequency': count,
            'percentage': count / len(paths) * 100
        }
        for p, count in sorted_patterns
    ]


# Example:
patterns = detect_path_patterns(graph, all_paths)
# Returns: [
#   {'pattern': 'Person → Company → Location', 'frequency': 3, 'percentage': 60%}
# ]
```

---

## Performance Optimization Patterns

### Pattern 13: Path Caching

Cache frequently computed paths.

**Use Case:** Repeated queries on static graphs

**Implementation:**
```python
class CachedPathFinder:
    def __init__(self, graph):
        self.graph = graph
        self.path_cache = {}
    
    def find_shortest_path(self, source, target):
        """Find path with caching."""
        cache_key = (source, target)
        
        if cache_key in self.path_cache:
            return self.path_cache[cache_key]
        
        path = self._find_shortest_path_impl(source, target)
        self.path_cache[cache_key] = path
        return path
    
    def _find_shortest_path_impl(self, source, target):
        # Implementation
        pass
    
    def clear_cache(self):
        self.path_cache.clear()
```

---

### Pattern 14: Bidirectional Search

Search from both source and target simultaneously.

**Use Case:** Faster path finding in large graphs

**Implementation:**
```python
def find_path_bidirectional(graph, source, target):
    """
    Find path by searching from both ends simultaneously.
    
    Complexity: O(√(V + E)) - square root improvement
    """
    from collections import deque
    
    if source == target:
        return [source]
    
    # Forward search
    forward_visited = {source: [source]}
    forward_queue = deque([source])
    
    # Backward search
    backward_visited = {target: [target]}
    backward_queue = deque([target])
    
    while forward_queue or backward_queue:
        # Forward step
        if forward_queue:
            current = forward_queue.popleft()
            for neighbor in graph.get(current, []):
                if neighbor in backward_visited:
                    # Found connection!
                    return forward_visited[current] + backward_visited[neighbor][::-1]
                
                if neighbor not in forward_visited:
                    forward_visited[neighbor] = forward_visited[current] + [neighbor]
                    forward_queue.append(neighbor)
        
        # Backward step
        if backward_queue:
            current = backward_queue.popleft()
            for neighbor in graph.get(current, []):
                if neighbor in forward_visited:
                    # Found connection!
                    return forward_visited[neighbor] + backward_visited[current][::-1]
                
                if neighbor not in backward_visited:
                    backward_visited[neighbor] = backward_visited[current] + [neighbor]
                    backward_queue.append(neighbor)
    
    return None  # No path found
```

---

## Explanation Generation Patterns

### Pattern 15: Natural Language Path Explanation

Convert paths to human-readable explanations.

**Use Case:** Explainability, user-friendly output

**Implementation:**
```python
def generate_path_explanation(graph, path):
    """
    Convert path to natural language explanation.
    
    Args:
        path: List of node IDs
    
    Returns:
        Natural language description
    """
    if not path or len(path) < 2:
        return "No path found"
    
    sentences = []
    
    for i in range(len(path) - 1):
        source = path[i]
        target = path[i + 1]
        edge = graph.get_edge(source, target)
        rel_type = edge.get('type', 'connected_to')
        
        # Template matching
        templates = {
            'works_at': f"{source} works at {target}",
            'partner_of': f"{source} partners with {target}",
            'located_in': f"{source} is located in {target}",
            'owns': f"{source} owns {target}",
        }
        
        sentence = templates.get(rel_type, f"{source} {rel_type} {target}")
        sentences.append(sentence)
    
    # Join sentences
    explanation = ". ".join(sentences) + "."
    
    # Add conclusion
    conclusion = f"Therefore, {path[0]} is connected to {path[-1]} through {len(path) - 2} intermediate connections."
    
    return explanation + " " + conclusion


# Example:
path = ["Alice", "Acme", "BetaCorp"]
explanation = generate_path_explanation(graph, path)
# Returns: "Alice works at Acme. Acme partners with BetaCorp. Therefore, Alice is connected to BetaCorp..."
```

---

## Summary

| Pattern | Algorithm | Complexity | Best Use |
|---------|-----------|-----------|----------|
| 1. Shortest Path | BFS | O(V+E) | Direct connections |
| 2. Weighted Path | Dijkstra | O((V+E)logV) | Confidence paths |
| 3. All Paths | DFS | O(V*paths) | Complete enumeration |
| 4. K-Shortest | Modified Dijkstra | O(K*ElogV) | Multiple alternatives |
| 5. Distance Rank | Sort | O(PlogP) | Shortest first |
| 6. Confidence Rank | Scoring | O(P*L) | Certain first |
| 7. Composite Rank | Multi-criteria | O(P*L) | Balanced ranking |
| 8. Type Filter | Traversal | O(P*L) | Domain-specific |
| 9. Confidence Filter | Threshold | O(P*L) | Quality control |
| 10. Depth Limit | Filter | O(P) | Control complexity |
| 11. Diversity | Graph analysis | O(P*L) | Robustness |
| 12. Pattern Detect | Clustering | O(P*L) | Common structures |
| 13. Caching | Hash lookup | O(1) | Performance |
| 14. Bidirectional | Dual BFS | O(√E) | Fast discovery |
| 15. Explanation | Template | O(L) | User-friendly |


