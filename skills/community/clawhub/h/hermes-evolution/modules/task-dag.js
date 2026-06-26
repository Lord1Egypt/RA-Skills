/**
 * TaskDAG - P2-2 任务依赖增强
 * 从简单依赖数组 → DAG（有向无环图）+ 拓扑排序
 * 
 * 支持：
 * 1. DAG 构建 - 节点和边的管理
 * 2. 拓扑排序 - 按依赖顺序执行
 * 3. 循环检测 - 防止无限循环
 * 4. 可视化 - 生成依赖关系图
 * 5. 并行优化 - 识别可并行执行的任务组
 */

class TaskDAG {
  constructor() {
    this.nodes = new Map();  // nodeId -> { id, data, inDegree, outEdges }
    this.edges = [];         // [{ from, to }]
    this.sorted = null;      // 缓存拓扑排序结果
  }

  /**
   * 添加节点
   */
  addNode(id, data = {}) {
    if (this.nodes.has(id)) {
      throw new Error(`节点 ${id} 已存在`);
    }
    
    this.nodes.set(id, {
      id,
      data,
      inDegree: 0,
      outEdges: []
    });
    
    this.sorted = null;  // 使缓存失效
    return this;
  }

  /**
   * 添加边（依赖关系）
   */
  addEdge(from, to) {
    if (!this.nodes.has(from)) {
      throw new Error(`源节点 ${from} 不存在`);
    }
    if (!this.nodes.has(to)) {
      throw new Error(`目标节点 ${to} 不存在`);
    }
    
    // 检查是否已存在这条边
    if (this.edges.some(e => e.from === from && e.to === to)) {
      return this;  // 忽略重复边
    }
    
    this.edges.push({ from, to });
    this.nodes.get(to).inDegree++;
    this.nodes.get(from).outEdges.push(to);
    
    this.sorted = null;  // 使缓存失效
    return this;
  }

  /**
   * 检查是否有循环（DFS）
   */
  hasCycle() {
    const visited = new Set();
    const recStack = new Set();

    const dfs = (nodeId) => {
      visited.add(nodeId);
      recStack.add(nodeId);

      const node = this.nodes.get(nodeId);
      for (const neighbor of node.outEdges) {
        if (!visited.has(neighbor)) {
          if (dfs(neighbor)) return true;
        } else if (recStack.has(neighbor)) {
          return true;
        }
      }

      recStack.delete(nodeId);
      return false;
    };

    for (const nodeId of this.nodes.keys()) {
      if (!visited.has(nodeId)) {
        if (dfs(nodeId)) return true;
      }
    }

    return false;
  }

  /**
   * 获取拓扑排序（Kahn算法）
   */
  topologicalSort() {
    if (this.hasCycle()) {
      throw new Error('图中存在循环，无法进行拓扑排序');
    }

    if (this.sorted) {
      return this.sorted;  // 返回缓存结果
    }

    // 复制入度
    const inDegree = new Map();
    for (const [id, node] of this.nodes) {
      inDegree.set(id, node.inDegree);
    }

    // 从入度为0的节点开始（队列）
    const queue = [];
    for (const [id, degree] of inDegree) {
      if (degree === 0) queue.push(id);
    }

    const sorted = [];

    while (queue.length > 0) {
      const current = queue.shift();
      sorted.push(current);

      const node = this.nodes.get(current);
      for (const neighbor of node.outEdges) {
        const newDegree = inDegree.get(neighbor) - 1;
        inDegree.set(neighbor, newDegree);
        if (newDegree === 0) {
          queue.push(neighbor);
        }
      }
    }

    this.sorted = sorted;
    return sorted;
  }

  /**
   * 获取可并行执行的任务组
   * 按执行批次分组，每组内任务可并行
   */
  getParallelBatches() {
    if (this.hasCycle()) {
      throw new Error('图中存在循环');
    }

    const batches = [];
    const completed = new Set();
    const inDegree = new Map();

    // 初始化入度
    for (const [id, node] of this.nodes) {
      inDegree.set(id, node.inDegree);
    }

    while (completed.size < this.nodes.size) {
      // 找出入度为0且未完成的任务
      const batch = [];
      for (const [id, degree] of inDegree) {
        if (degree === 0 && !completed.has(id)) {
          batch.push(id);
        }
      }

      if (batch.length === 0 && completed.size < this.nodes.size) {
        throw new Error('依赖图中存在循环');
      }

      batches.push(batch);

      // 标记这批任务完成，更新入度
      for (const id of batch) {
        completed.add(id);
        const node = this.nodes.get(id);
        for (const neighbor of node.outEdges) {
          inDegree.set(neighbor, inDegree.get(neighbor) - 1);
        }
      }
    }

    return batches;
  }

  /**
   * 获取节点数据
   */
  getNode(id) {
    return this.nodes.get(id);
  }

  /**
   * 获取节点的依赖（前置任务）
   */
  getDependencies(id) {
    const node = this.nodes.get(id);
    if (!node) return [];

    const deps = [];
    for (const edge of this.edges) {
      if (edge.to === id) {
        deps.push(edge.from);
      }
    }
    return deps;
  }

  /**
   * 获取节点的反向依赖（后继任务）
   */
  getDependents(id) {
    const node = this.nodes.get(id);
    if (!node) return [];
    return [...node.outEdges];
  }

  /**
   * 可视化：生成文本依赖图
   */
  visualize() {
    const lines = [];
    lines.push('\n📊 DAG 可视化\n');
    lines.push('═'.repeat(60));

    const batches = this.getParallelBatches();

    for (let i = 0; i < batches.length; i++) {
      const batch = batches[i];
      const batchNum = i + 1;
      
      lines.push(`\n【批次 ${batchNum}】${batch.length === 1 ? '🔹' : '🔸'} ${batch.length > 1 ? '可并行' : '串行'}`);
      
      for (const nodeId of batch) {
        const node = this.nodes.get(nodeId);
        const deps = this.getDependencies(nodeId);
        const dependents = this.getDependents(nodeId);
        
        const label = node.data.label || nodeId;
        const status = node.data.status || '-';
        
        lines.push(`  📌 ${label}`);
        lines.push(`     状态: ${status}`);
        
        if (deps.length > 0) {
          lines.push(`     ← 依赖: ${deps.map(d => this.nodes.get(d).data.label || d).join(', ')}`);
        }
        if (dependents.length > 0) {
          lines.push(`     → 影响: ${dependents.map(d => this.nodes.get(d).data.label || d).join(', ')}`);
        }
      }
    }

    lines.push('\n' + '═'.repeat(60));
    lines.push(`\n📈 统计: ${this.nodes.size} 个节点, ${this.edges.length} 条边`);
    lines.push(`\n🔄 循环检测: ${this.hasCycle() ? '❌ 存在循环' : '✅ 无循环'}`);

    return lines.join('\n');
  }

  /**
   * 生成 DOT 语言（可用于 Graphviz）
   */
  toDOT() {
    let dot = 'digraph TaskDAG {\n';
    dot += '  rankdir=TB;\n';
    dot += '  node [shape=box];\n\n';

    for (const [id, node] of this.nodes) {
      const label = node.data.label || id;
      const status = node.data.status || 'pending';
      const color = status === 'done' ? 'green' : status === 'failed' ? 'red' : 'gray';
      dot += `  "${id}" [label="${label}" color=${color}];\n`;
    }

    dot += '\n';

    for (const edge of this.edges) {
      dot += `  "${edge.from}" -> "${edge.to}";\n`;
    }

    dot += '}\n';
    return dot;
  }

  /**
   * 从任务列表构建 DAG
   */
  static fromTasks(tasks) {
    const dag = new TaskDAG();

    // 添加所有节点
    for (const task of tasks) {
      dag.addNode(task.id, {
        label: task.label || task.title || task.id,
        status: task.status || 'pending',
        ...task
      });
    }

    // 添加边
    for (const task of tasks) {
      if (task.dependsOn && Array.isArray(task.dependsOn)) {
        for (const depId of task.dependsOn) {
          try {
            dag.addEdge(depId, task.id);
          } catch (e) {
            // 忽略无效依赖
          }
        }
      }
    }

    return dag;
  }
}

// 导出
module.exports = { TaskDAG };
