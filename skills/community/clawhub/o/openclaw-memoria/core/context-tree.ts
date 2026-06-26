/**
 * Memoria — Layer 6: Context Tree
 * 
 * Organizes facts into a semantic hierarchy for structured recall.
 * Instead of "here are 8 flat facts", we inject:
 * 
 * Bureau (3 faits)
 *   ├─ CRM (2 faits)
 *   └─ Modules (1 fait)
 * Convex (2 faits)
 * Infrastructure (3 faits)
 * 
 * Permet de :
 * 1. Montrer la STRUCTURE de la mémoire
 * 2. Prioriser par branche (Bureau > infra si query mentionne "CRM")
 * 3. Éviter l'overload de faits non pertinents
 */

import type { MemoriaDB, Fact } from "./db.js";

// ─── Types ───

export interface ContextNode {
  id: string;
  label: string;              // "Bureau", "CRM", "Modules"...
  type: "root" | "branch" | "leaf";
  facts: string[];            // Fact IDs
  children: ContextNode[];
  weight: number;             // Relevance to current query
  depth: number;
  parent?: ContextNode;
}

export interface ContextTree {
  roots: ContextNode[];
  factMap: Map<string, ContextNode>; // fact ID → node containing it
}

// ─── Builder ───

export class ContextTreeBuilder {
  private db: MemoriaDB;

  constructor(db: MemoriaDB) {
    this.db = db;
  }

  /** Build a context tree from a list of facts */
  async build(facts: Fact[], query?: string): Promise<ContextTree> {
    if (facts.length === 0) {
      return { roots: [], factMap: new Map() };
    }

    // Step 1: Cluster by category + keyword heuristics (no LLM)
    const clusters = await this.clusterFacts(facts);

    // Step 2: Build tree structure
    const roots: ContextNode[] = [];
    const factMap = new Map<string, ContextNode>();

    for (const cluster of clusters) {
      const node = this.buildNode(cluster, 0);
      roots.push(node);
      this.indexFactMap(node, factMap);
    }

    // Step 3: Weight by query relevance (if provided)
    if (query) {
      this.weightByQuery(roots, query);
    }

    return { roots, factMap };
  }

  /** Render tree as indented text */
  renderTree(tree: ContextTree, maxDepth = 3): string {
    const lines: string[] = [];

    const render = (node: ContextNode, indent = "") => {
      if (node.depth > maxDepth) return;

      const prefix = node.depth === 0 ? "▪" : node.type === "branch" ? "├─" : "  ";
      const weight = node.weight > 0 ? ` [${node.weight.toFixed(2)}]` : "";
      const factCount = node.facts.length > 0 ? ` (${node.facts.length})` : "";
      
      lines.push(`${indent}${prefix} ${node.label}${weight}${factCount}`);

      for (let i = 0; i < node.children.length; i++) {
        const child = node.children[i];
        const childIndent = indent + (node.depth === 0 ? "  " : "  ");
        render(child, childIndent);
      }
    };

    for (const root of tree.roots) {
      render(root);
    }

    return lines.join("\n");
  }

  /** Get facts from tree in priority order (high weight first) */
  extractFacts(tree: ContextTree, limit: number): Fact[] {
    // Flatten all nodes with facts
    const nodesWithFacts: Array<{ node: ContextNode; factIds: string[] }> = [];

    const collect = (node: ContextNode) => {
      if (node.facts.length > 0) {
        nodesWithFacts.push({ node, factIds: node.facts });
      }
      for (const child of node.children) {
        collect(child);
      }
    };

    for (const root of tree.roots) {
      collect(root);
    }

    // Sort by weight (high → low)
    nodesWithFacts.sort((a, b) => b.node.weight - a.node.weight);

    // Extract facts up to limit
    const factIds = new Set<string>();
    const results: Fact[] = [];

    for (const { factIds: ids } of nodesWithFacts) {
      for (const id of ids) {
        if (factIds.has(id)) continue;
        factIds.add(id);

        const fact = this.db.getFact(id);
        if (fact && !fact.superseded) {
          results.push(fact);
          if (results.length >= limit) return results;
        }
      }
    }

    return results;
  }

  // ─── Private ───

  private async clusterFacts(facts: Fact[]): Promise<Cluster[]> {
    // Use categories + keywords for initial grouping
    const grouped = new Map<string, Fact[]>();

    for (const fact of facts) {
      const category = fact.category || "other";
      if (!grouped.has(category)) grouped.set(category, []);
      grouped.get(category)!.push(fact);
    }

    // Build clusters
    const clusters: Cluster[] = [];

    for (const [category, catFacts] of grouped) {
      if (catFacts.length === 0) continue;

      // If too many facts in one category, sub-cluster by keywords
      if (catFacts.length > 10) {
        const subClusters = this.subClusterByKeywords(catFacts);
        clusters.push({
          label: this.categoryLabel(category),
          facts: [],
          children: subClusters,
        });
      } else {
        clusters.push({
          label: this.categoryLabel(category),
          facts: catFacts,
          children: [],
        });
      }
    }

    return clusters;
  }

  private subClusterByKeywords(facts: Fact[]): Cluster[] {
    // Extract common keywords
    const keywordMap = new Map<string, Fact[]>();

    for (const fact of facts) {
      const words = this.extractKeywords(fact.fact);
      for (const word of words) {
        if (!keywordMap.has(word)) keywordMap.set(word, []);
        keywordMap.get(word)!.push(fact);
      }
    }

    // Take top keywords (most frequent)
    const sorted = Array.from(keywordMap.entries())
      .sort((a, b) => b[1].length - a[1].length)
      .slice(0, 5);

    const clusters: Cluster[] = [];
    const assigned = new Set<string>();

    for (const [keyword, keywordFacts] of sorted) {
      const unique = keywordFacts.filter(f => !assigned.has(f.id));
      if (unique.length === 0) continue;

      clusters.push({
        label: keyword,
        facts: unique,
        children: [],
      });

      for (const f of unique) assigned.add(f.id);
    }

    // Remaining = "Autres"
    const remaining = facts.filter(f => !assigned.has(f.id));
    if (remaining.length > 0) {
      clusters.push({
        label: "Autres",
        facts: remaining,
        children: [],
      });
    }

    return clusters;
  }

  private extractKeywords(text: string): string[] {
    // Simple keyword extraction (proper nouns + technical terms)
    const stopWords = new Set([
      "le", "la", "les", "un", "une", "des", "de", "du", "et", "ou", "à", "dans", "pour", "sur", "avec", "est", "sont",
      "a", "an", "the", "and", "or", "to", "in", "for", "on", "with", "is", "are", "was", "were", "been", "be",
    ]);

    const words = text.split(/\s+/)
      .map(w => w.replace(/[^\p{L}\p{N}]/gu, "").toLowerCase())
      .filter(w => w.length > 3 && !stopWords.has(w));

    // Capitalize proper nouns (heuristic: starts uppercase in original)
    const properNouns = text.match(/\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b/g) || [];
    const allKeywords = [...words, ...properNouns.map(w => w.toLowerCase())];

    // Return unique, most common
    const freq = new Map<string, number>();
    for (const w of allKeywords) {
      freq.set(w, (freq.get(w) || 0) + 1);
    }

    return Array.from(freq.keys())
      .sort((a, b) => freq.get(b)! - freq.get(a)!)
      .slice(0, 5);
  }

  private buildNode(cluster: Cluster, depth: number): ContextNode {
    const node: ContextNode = {
      id: `node_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`,
      label: cluster.label,
      type: depth === 0 ? "root" : cluster.children.length > 0 ? "branch" : "leaf",
      facts: cluster.facts.map(f => f.id),
      children: [],
      weight: 0,
      depth,
    };

    for (const child of cluster.children) {
      const childNode = this.buildNode(child, depth + 1);
      childNode.parent = node;
      node.children.push(childNode);
    }

    return node;
  }

  private indexFactMap(node: ContextNode, map: Map<string, ContextNode>) {
    for (const factId of node.facts) {
      map.set(factId, node);
    }
    for (const child of node.children) {
      this.indexFactMap(child, map);
    }
  }

  private weightByQuery(roots: ContextNode[], query: string) {
    const lowerQuery = query.toLowerCase();
    const words = lowerQuery.split(/\s+/).filter(w => w.length > 2);

    const weight = (node: ContextNode) => {
      const labelLower = node.label.toLowerCase();
      let score = 0;

      // Exact label match
      if (lowerQuery.includes(labelLower) || labelLower.includes(lowerQuery)) {
        score += 1.0;
      }

      // Word overlap
      for (const word of words) {
        if (labelLower.includes(word)) {
          score += 0.3;
        }
      }

      node.weight = score;

      // Recurse children
      for (const child of node.children) {
        weight(child);
        // Propagate child weight to parent
        node.weight += child.weight * 0.5;
      }
    };

    for (const root of roots) {
      weight(root);
    }
  }

  private categoryLabel(cat: string): string {
    const labels: Record<string, string> = {
      outil: "Outils",
      savoir: "Savoir",
      erreur: "Erreurs",
      client: "Clients",
      preference: "Préférences",
      chronologie: "Chronologie",
      rh: "RH",
    };
    return labels[cat] || cat.charAt(0).toUpperCase() + cat.slice(1);
  }
}

// ─── Internal types ───

interface Cluster {
  label: string;
  facts: Fact[];
  children: Cluster[];
}
