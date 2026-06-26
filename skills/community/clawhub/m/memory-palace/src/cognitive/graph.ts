/**
 * Knowledge Graph
 * 
 * Build and maintain a knowledge graph from memories.
 */

import type { Memory } from '../types.js';

/**
 * Graph node
 */
export interface GraphNode {
  /** Node ID */
  id: string;
  
  /** Node label */
  label: string;
  
  /** Node type */
  type: 'memory' | 'entity' | 'tag' | 'location' | 'concept';
  
  /** Associated memory IDs */
  memoryIds: string[];
  
  /** Node properties */
  properties: Record<string, unknown>;
}

/**
 * Graph edge
 */
export interface GraphEdge {
  /** Source node ID */
  source: string;
  
  /** Target node ID */
  target: string;
  
  /** Edge type */
  type: 'mentions' | 'related' | 'tagged' | 'located' | 'similar' | 'follows';
  
  /** Edge weight (0-1) */
  weight: number;
  
  /** Edge properties */
  properties?: Record<string, unknown>;
}

/**
 * Knowledge graph
 */
export interface KnowledgeGraph {
  /** All nodes */
  nodes: GraphNode[];
  
  /** All edges */
  edges: GraphEdge[];
  
  /** Node lookup by ID */
  nodeMap: Map<string, GraphNode>;
  
  /** Adjacency list for quick neighbor lookup */
  adjacency: Map<string, Set<string>>;
}

/**
 * Graph traversal options
 */
export interface TraversalOptions {
  /** Maximum depth */
  maxDepth?: number;
  
  /** Edge types to follow */
  edgeTypes?: GraphEdge['type'][];
  
  /** Node types to include */
  nodeTypes?: GraphNode['type'][];
}

/**
 * Knowledge graph builder
 */
export class KnowledgeGraphBuilder {
  /**
   * Build a knowledge graph from memories
   */
  async build(memories: Memory[]): Promise<KnowledgeGraph> {
    const nodes: GraphNode[] = [];
    const edges: GraphEdge[] = [];
    const nodeMap = new Map<string, GraphNode>();
    const adjacency = new Map<string, Set<string>>();
    
    // Create memory nodes
    for (const memory of memories) {
      const node: GraphNode = {
        id: `memory:${memory.id}`,
        label: memory.summary || memory.content.slice(0, 50),
        type: 'memory',
        memoryIds: [memory.id],
        properties: {
          importance: memory.importance,
          status: memory.status,
          source: memory.source,
          createdAt: memory.createdAt,
        },
      };
      nodes.push(node);
      nodeMap.set(node.id, node);
      adjacency.set(node.id, new Set());
    }
    
    // Create tag nodes and edges
    const tagNodes = new Map<string, GraphNode>();
    for (const memory of memories) {
      for (const tag of memory.tags) {
        if (!tagNodes.has(tag)) {
          const node: GraphNode = {
            id: `tag:${tag}`,
            label: tag,
            type: 'tag',
            memoryIds: [],
            properties: { count: 0 },
          };
          tagNodes.set(tag, node);
          nodes.push(node);
          nodeMap.set(node.id, node);
          adjacency.set(node.id, new Set());
        }
        
        const tagNode = tagNodes.get(tag)!;
        tagNode.memoryIds.push(memory.id);
        tagNode.properties.count = (tagNode.properties.count as number) + 1;
        
        // Create edge
        const edge: GraphEdge = {
          source: `memory:${memory.id}`,
          target: `tag:${tag}`,
          type: 'tagged',
          weight: memory.importance,
        };
        edges.push(edge);
        
        adjacency.get(`memory:${memory.id}`)!.add(`tag:${tag}`);
        adjacency.get(`tag:${tag}`)!.add(`memory:${memory.id}`);
      }
    }
    
    // Create location nodes and edges
    const locationNodes = new Map<string, GraphNode>();
    for (const memory of memories) {
      const location = memory.location;
      if (!locationNodes.has(location)) {
        const node: GraphNode = {
          id: `location:${location}`,
          label: location,
          type: 'location',
          memoryIds: [],
          properties: { count: 0 },
        };
        locationNodes.set(location, node);
        nodes.push(node);
        nodeMap.set(node.id, node);
        adjacency.set(node.id, new Set());
      }
      
      const locationNode = locationNodes.get(location)!;
      locationNode.memoryIds.push(memory.id);
      locationNode.properties.count = (locationNode.properties.count as number) + 1;
      
      // Create edge
      const edge: GraphEdge = {
        source: `memory:${memory.id}`,
        target: `location:${location}`,
        type: 'located',
        weight: 1,
      };
      edges.push(edge);
      
      adjacency.get(`memory:${memory.id}`)!.add(`location:${location}`);
      adjacency.get(`location:${location}`)!.add(`memory:${memory.id}`);
    }
    
    // Create similarity edges between memories with shared tags
    for (let i = 0; i < memories.length; i++) {
      for (let j = i + 1; j < memories.length; j++) {
        const memA = memories[i];
        const memB = memories[j];
        
        // Calculate tag overlap
        const sharedTags = memA.tags.filter(t => memB.tags.includes(t));
        if (sharedTags.length > 0) {
          const weight = sharedTags.length / Math.max(memA.tags.length, memB.tags.length);
          
          // Only create edge if overlap is significant
          if (weight >= 0.3) {
            edges.push({
              source: `memory:${memA.id}`,
              target: `memory:${memB.id}`,
              type: 'similar',
              weight,
              properties: { sharedTags },
            });
            
            adjacency.get(`memory:${memA.id}`)!.add(`memory:${memB.id}`);
            adjacency.get(`memory:${memB.id}`)!.add(`memory:${memA.id}`);
          }
        }
      }
    }
    
    return { nodes, edges, nodeMap, adjacency };
  }
  
  /**
   * Get neighbors of a node
   */
  getNeighbors(graph: KnowledgeGraph, nodeId: string, options: TraversalOptions = {}): GraphNode[] {
    const neighbors = graph.adjacency.get(nodeId);
    if (!neighbors) return [];
    
    const result: GraphNode[] = [];
    const edgeTypes = options.edgeTypes;
    const nodeTypes = options.nodeTypes;
    
    for (const neighborId of neighbors) {
      const node = graph.nodeMap.get(neighborId);
      if (!node) continue;
      
      // Filter by node type
      if (nodeTypes && !nodeTypes.includes(node.type)) continue;
      
      // Filter by edge type
      if (edgeTypes) {
        const edge = graph.edges.find(e => 
          (e.source === nodeId && e.target === neighborId) ||
          (e.target === nodeId && e.source === neighborId)
        );
        if (edge && !edgeTypes.includes(edge.type)) continue;
      }
      
      result.push(node);
    }
    
    return result;
  }
  
  /**
   * Find path between two nodes (BFS)
   */
  findPath(graph: KnowledgeGraph, fromId: string, toId: string, options: TraversalOptions = {}): GraphNode[] {
    const maxDepth = options.maxDepth || 5;
    const visited = new Set<string>();
    const queue: { id: string; path: GraphNode[] }[] = [
      { id: fromId, path: [graph.nodeMap.get(fromId)!].filter(Boolean) }
    ];
    
    while (queue.length > 0) {
      const current = queue.shift()!;
      
      if (current.id === toId) {
        return current.path;
      }
      
      if (current.path.length >= maxDepth) continue;
      if (visited.has(current.id)) continue;
      visited.add(current.id);
      
      const neighbors = this.getNeighbors(graph, current.id, options);
      for (const neighbor of neighbors) {
        if (!visited.has(neighbor.id)) {
          queue.push({
            id: neighbor.id,
            path: [...current.path, neighbor],
          });
        }
      }
    }
    
    return []; // No path found
  }
  
  /**
   * Get subgraph centered on a node
   */
  getSubgraph(graph: KnowledgeGraph, centerId: string, depth: number = 2): KnowledgeGraph {
    const visited = new Set<string>();
    const nodes: GraphNode[] = [];
    const edges: GraphEdge[] = [];
    const nodeMap = new Map<string, GraphNode>();
    const adjacency = new Map<string, Set<string>>();
    
    const traverse = (nodeId: string, currentDepth: number) => {
      if (visited.has(nodeId) || currentDepth > depth) return;
      visited.add(nodeId);
      
      const node = graph.nodeMap.get(nodeId);
      if (!node) return;
      
      nodes.push(node);
      nodeMap.set(nodeId, node);
      adjacency.set(nodeId, new Set());
      
      if (currentDepth < depth) {
        const neighbors = this.getNeighbors(graph, nodeId);
        for (const neighbor of neighbors) {
          traverse(neighbor.id, currentDepth + 1);
          
          // Add edge
          const edge = graph.edges.find(e =>
            (e.source === nodeId && e.target === neighbor.id) ||
            (e.target === nodeId && e.source === neighbor.id)
          );
          if (edge) {
            edges.push(edge);
            adjacency.get(nodeId)!.add(neighbor.id);
            if (!adjacency.has(neighbor.id)) {
              adjacency.set(neighbor.id, new Set());
            }
            adjacency.get(neighbor.id)!.add(nodeId);
          }
        }
      }
    };
    
    traverse(centerId, 0);
    
    return { nodes, edges, nodeMap, adjacency };
  }
  
  /**
   * Export graph to a simple format for visualization
   */
  exportForVisualization(graph: KnowledgeGraph): { nodes: Array<{ id: string; label: string; type: string }>; edges: Array<{ source: string; target: string; type: string }> } {
    return {
      nodes: graph.nodes.map(n => ({
        id: n.id,
        label: n.label,
        type: n.type,
      })),
      edges: graph.edges.map(e => ({
        source: e.source,
        target: e.target,
        type: e.type,
      })),
    };
  }
}