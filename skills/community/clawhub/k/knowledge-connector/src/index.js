const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');

class KnowledgeConnector {
  constructor(options = {}) {
    this.dataDir = options.dataDir || process.env.KC_DATA_DIR || path.join(os.homedir(), '.local', 'share', 'knowledge-connector');
    this.conceptsFile = path.join(this.dataDir, 'concepts.json');
    this.relationsFile = path.join(this.dataDir, 'relations.json');
    this.sourcesFile = path.join(this.dataDir, 'sources.json');
    this.initError = null;
    this.init();
  }

  init() {
    try {
      if (!fs.existsSync(this.dataDir)) {
        fs.mkdirSync(this.dataDir, { recursive: true });
      }
      for (const file of [this.conceptsFile, this.relationsFile, this.sourcesFile]) {
        if (!fs.existsSync(file)) {
          fs.writeFileSync(file, JSON.stringify([]));
        }
      }
    } catch (error) {
      this.initError = error;
    }
  }

  loadJson(file) {
    try {
      return JSON.parse(fs.readFileSync(file, 'utf-8'));
    } catch {
      return [];
    }
  }

  saveJson(file, data) {
    fs.writeFileSync(file, JSON.stringify(data, null, 2));
  }

  loadConcepts() {
    return this.loadJson(this.conceptsFile);
  }

  saveConceptsData(concepts) {
    this.saveJson(this.conceptsFile, concepts);
  }

  loadRelations() {
    return this.loadJson(this.relationsFile);
  }

  saveRelationsData(relations) {
    this.saveJson(this.relationsFile, relations);
  }

  loadSources() {
    return this.loadJson(this.sourcesFile);
  }

  saveSourcesData(sources) {
    this.saveJson(this.sourcesFile, sources);
  }

  generateId() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  hashText(value) {
    return crypto.createHash('sha256').update(String(value || '')).digest('hex');
  }

  normalizeName(name) {
    return String(name || '').trim().toLowerCase();
  }

  canonicalPath(filePath) {
    try {
      return fs.realpathSync.native(filePath);
    } catch {
      return path.resolve(filePath);
    }
  }

  getSourceExcerpt(text) {
    return String(text || '').replace(/\s+/g, ' ').trim().slice(0, 160);
  }

  getKnownTerms() {
    return [
      '人工智能', '机器学习', '强化学习', '深度学习', '神经网络', '自然语言处理',
      '计算机视觉', '数据挖掘', '知识图谱', '知识库', '跨文档', '向量检索',
      '检索增强', '规划', '算法', '模型', '训练', '推理',
      'Python', 'JavaScript', 'Java', 'TypeScript', 'Node.js',
      'React', 'Vue', 'Angular', '数据库', 'API', '微服务',
      '云计算', '大数据', '区块链', '物联网', '5G', '边缘计算'
    ];
  }

  getStopWords() {
    return new Set([
      '这是', '那是', '一个', '一些', '可以', '进行', '需要', '通过', '根据', '关于',
      '哪些', '文档', '这个', '那个', '里面', '之间', '同时', '如何', '为什么',
      '以及', '还是', '是否', '什么', '怎么', '怎样', '起来', '连接', '相关'
    ]);
  }

  tokenizeText(text) {
    const raw = String(text || '');
    const tokens = new Set();
    const stopWords = this.getStopWords();
    const addToken = (token) => {
      const cleaned = String(token || '').trim().toLowerCase();
      if (!cleaned || cleaned.length < 2 || cleaned.length > 40 || stopWords.has(cleaned)) {
        return;
      }
      tokens.add(cleaned);
    };

    for (const term of this.getKnownTerms()) {
      if (raw.includes(term)) {
        addToken(term);
      }
    }

    const englishPattern = /[a-zA-Z][a-zA-Z0-9.+\-_/]{1,40}/g;
    let match;
    while ((match = englishPattern.exec(raw)) !== null) {
      addToken(match[0]);
    }

    if (typeof Intl !== 'undefined' && Intl.Segmenter) {
      const segmenter = new Intl.Segmenter('zh', { granularity: 'word' });
      for (const segment of segmenter.segment(raw)) {
        if (segment.isWordLike) {
          addToken(segment.segment);
        }
      }
    } else {
      const chinesePattern = /[\u4e00-\u9fa5]{2,10}/g;
      while ((match = chinesePattern.exec(raw)) !== null) {
        addToken(match[0]);
      }
    }

    return Array.from(tokens);
  }

  extractChineseTerms(text) {
    return this.tokenizeText(text).filter((token) => /[\u4e00-\u9fa5]/.test(token));
  }

  escapeHtml(value) {
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  escapeDotLabel(value) {
    return String(value || '').replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\r?\n/g, ' ');
  }

  safeJsonForScript(value) {
    return JSON.stringify(value)
      .replace(/</g, '\\u003c')
      .replace(/>/g, '\\u003e')
      .replace(/&/g, '\\u0026')
      .replace(/\u2028/g, '\\u2028')
      .replace(/\u2029/g, '\\u2029');
  }

  scoreText(fields, query, tokens) {
    const haystack = fields.filter(Boolean).join(' ').toLowerCase();
    let score = query && haystack.includes(query) ? 10 : 0;
    const matchedTerms = [];

    for (const token of tokens) {
      if (haystack.includes(token)) {
        score += token.length >= 4 ? 2 : 1;
        matchedTerms.push(token);
      }
    }

    return { score, matchedTerms };
  }

  getTextFiles(targetPath, recursive = true) {
    const allowed = new Set(['.txt', '.md', '.markdown', '.text', '.json', '.csv']);
    const results = [];
    const stat = fs.statSync(targetPath);

    if (stat.isFile()) {
      return allowed.has(path.extname(targetPath).toLowerCase()) ? [targetPath] : [];
    }

    const walk = (dir) => {
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          if (recursive) {
            walk(fullPath);
          }
          continue;
        }
        if (allowed.has(path.extname(fullPath).toLowerCase())) {
          results.push(fullPath);
        }
      }
    };

    walk(targetPath);
    return results;
  }

  planImport(inputs, options = {}) {
    const targets = Array.isArray(inputs) ? inputs : [inputs];
    const recursive = options.recursive !== false;
    const files = [];

    for (const target of targets) {
      for (const filePath of this.getTextFiles(target, recursive)) {
        files.push({
          path: filePath,
          title: path.basename(filePath),
          type: path.extname(filePath).replace('.', '') || 'text'
        });
      }
    }

    return {
      fileCount: files.length,
      files,
      supportedTypes: Array.from(new Set(files.map((file) => file.type))).sort()
    };
  }

  async extract(text, options = {}) {
    const source = options.source || 'direct-input';
    const sourceId = options.sourceId || null;
    const concepts = [];
    const addConcept = (name, type, description = '') => {
      const trimmed = String(name || '').trim();
      if (!trimmed || trimmed.length < 2 || trimmed.length > 60) {
        return;
      }
      if (concepts.find((c) => this.normalizeName(c.name) === this.normalizeName(trimmed))) {
        return;
      }
      concepts.push({
        id: this.generateId(),
        name: trimmed,
        type,
        description,
        source,
        sourceId,
        sourceExcerpt: this.getSourceExcerpt(text),
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      });
    };

    let match;
    const quotedPattern = /["""']([^"""']+)["""']/g;
    while ((match = quotedPattern.exec(text)) !== null) {
      addConcept(match[1], 'term');
    }

    const properNounPattern = /[A-Z][a-zA-Z0-9.+\-/\s]{1,30}(?=[\s,;.!?：，。！)]|$)/g;
    while ((match = properNounPattern.exec(text)) !== null) {
      addConcept(match[0], 'proper-noun');
    }

    for (const term of this.extractChineseTerms(text)) {
      addConcept(term, 'concept');
    }

    for (const term of this.getKnownTerms()) {
      if (text.includes(term)) {
        addConcept(term, 'tech');
      }
    }

    return concepts;
  }

  async saveConcepts(newConcepts) {
    const existing = this.loadConcepts();

    for (const incoming of newConcepts) {
      const match = existing.find((item) => this.normalizeName(item.name) === this.normalizeName(incoming.name));
      if (!match) {
        existing.push({
          ...incoming,
          aliases: incoming.aliases || [],
          sources: incoming.source ? [incoming.source] : [],
          sourceIds: incoming.sourceId ? [incoming.sourceId] : []
        });
        continue;
      }

      match.updatedAt = new Date().toISOString();
      match.description = match.description || incoming.description || '';
      match.type = match.type || incoming.type;
      match.aliases = Array.from(new Set([...(match.aliases || []), ...(incoming.aliases || [])]));
      match.sources = Array.from(new Set([...(match.sources || []), ...(incoming.source ? [incoming.source] : [])]));
      match.sourceIds = Array.from(new Set([...(match.sourceIds || []), ...(incoming.sourceId ? [incoming.sourceId] : [])]));
      if (!match.sourceExcerpt && incoming.sourceExcerpt) {
        match.sourceExcerpt = incoming.sourceExcerpt;
      }
    }

    this.saveConceptsData(existing);
    return existing;
  }

  async connect(options) {
    const { from, to, type = '相关', weight = 0.5, source = 'manual' } = options;
    const concepts = this.loadConcepts();
    const fromConcept = concepts.find((c) => this.normalizeName(c.name) === this.normalizeName(from));
    const toConcept = concepts.find((c) => this.normalizeName(c.name) === this.normalizeName(to));

    if (!fromConcept) {
      throw new Error(`源概念不存在: ${from}`);
    }
    if (!toConcept) {
      throw new Error(`目标概念不存在: ${to}`);
    }

    const relations = this.loadRelations();
    const existing = relations.find((r) => r.from === fromConcept.id && r.to === toConcept.id && r.type === type);
    if (existing) {
      return existing;
    }

    const relation = {
      id: this.generateId(),
      from: fromConcept.id,
      to: toConcept.id,
      type,
      weight,
      source,
      createdAt: new Date().toISOString()
    };

    relations.push(relation);
    this.saveRelationsData(relations);
    return relation;
  }

  calculateSimilarity(s1, s2) {
    const set1 = new Set(String(s1 || ''));
    const set2 = new Set(String(s2 || ''));
    const intersection = new Set([...set1].filter((x) => set2.has(x)));
    const union = new Set([...set1, ...set2]);
    return union.size === 0 ? 0 : intersection.size / union.size;
  }

  async autoConnect() {
    const concepts = this.loadConcepts();
    const relations = this.loadRelations();
    const newRelations = [];

    for (let i = 0; i < concepts.length; i += 1) {
      for (let j = i + 1; j < concepts.length; j += 1) {
        const a = concepts[i];
        const b = concepts[j];
        const existing = relations.find((r) =>
          (r.from === a.id && r.to === b.id) || (r.from === b.id && r.to === a.id)
        );
        if (existing) {
          continue;
        }

        const sharedSource = (a.sourceIds || []).some((sourceId) => (b.sourceIds || []).includes(sourceId)) ||
          (a.sources || []).some((source) => (b.sources || []).includes(source));
        const similarity = this.calculateSimilarity(a.name, b.name);
        const weight = sharedSource ? Math.max(0.45, similarity) : similarity;

        if (weight >= 0.3) {
          const relation = {
            id: this.generateId(),
            from: a.id,
            to: b.id,
            type: sharedSource ? '共现' : (weight > 0.7 ? '相似' : '相关'),
            weight,
            source: sharedSource ? 'shared-source' : 'name-similarity',
            createdAt: new Date().toISOString()
          };
          relations.push(relation);
          newRelations.push(relation);
        }
      }
    }

    this.saveRelationsData(relations);
    return newRelations;
  }

  async importRelations(data) {
    const relations = this.loadRelations();
    const concepts = this.loadConcepts();
    const newRelations = [];

    for (const item of data) {
      const fromConcept = concepts.find((c) => c.name === item.from || c.id === item.from);
      const toConcept = concepts.find((c) => c.name === item.to || c.id === item.to);
      if (!fromConcept || !toConcept) {
        continue;
      }
      const relationType = item.type || '相关';
      const existing = relations.find((r) => r.from === fromConcept.id && r.to === toConcept.id && r.type === relationType);
      if (existing) {
        continue;
      }
      const relation = {
        id: this.generateId(),
        from: fromConcept.id,
        to: toConcept.id,
        type: relationType,
        weight: item.weight || 0.5,
        source: item.source || 'import',
        createdAt: new Date().toISOString()
      };
      relations.push(relation);
      newRelations.push(relation);
    }

    this.saveRelationsData(relations);
    return newRelations;
  }

  async importDocuments(inputs, options = {}) {
    const targets = Array.isArray(inputs) ? inputs : [inputs];
    const recursive = options.recursive !== false;
    const sources = this.loadSources();
    const importedFiles = [];
    let conceptCount = 0;
    let newSourceCount = 0;
    let updatedSourceCount = 0;

    for (const target of targets) {
      for (const filePath of this.getTextFiles(target, recursive)) {
        const content = fs.readFileSync(filePath, 'utf-8');
        const canonical = this.canonicalPath(filePath);
        const contentHash = this.hashText(content);
        const existingIndex = sources.findIndex((source) =>
          source.sourceKey === canonical ||
          source.canonicalPath === canonical ||
          (source.path && this.canonicalPath(source.path) === canonical)
        );
        const existingSource = existingIndex >= 0 ? sources[existingIndex] : null;
        const now = new Date().toISOString();
        const sourceRecord = {
          ...(existingSource || {}),
          id: existingSource ? existingSource.id : `src-${this.hashText(canonical).slice(0, 32)}`,
          title: path.basename(filePath),
          path: filePath,
          canonicalPath: canonical,
          sourceKey: canonical,
          contentHash,
          type: path.extname(filePath).replace('.', '') || 'text',
          excerpt: this.getSourceExcerpt(content),
          importedAt: existingSource ? existingSource.importedAt : now,
          updatedAt: now
        };

        const concepts = await this.extract(content, { source: sourceRecord.title, sourceId: sourceRecord.id });
        await this.saveConcepts(concepts);
        sourceRecord.conceptCount = concepts.length;
        if (existingIndex >= 0) {
          sources[existingIndex] = sourceRecord;
          updatedSourceCount += 1;
        } else {
          sources.push(sourceRecord);
          newSourceCount += 1;
        }
        importedFiles.push(sourceRecord);
        conceptCount += concepts.length;
      }
    }

    this.saveSourcesData(sources);
    const relations = options.autoConnect === false ? [] : await this.autoConnect();

    return {
      fileCount: importedFiles.length,
      conceptCount,
      relationCount: relations.length,
      newSourceCount,
      updatedSourceCount,
      files: importedFiles
    };
  }

  async search(keyword, options = {}) {
    const query = String(keyword || '').trim().toLowerCase();
    const concepts = this.loadConcepts();
    const sources = this.loadSources();
    const relations = this.loadRelations();
    const conceptNames = concepts
      .map((concept) => concept.name)
      .filter((name) => name && String(name).length >= 2 && query.includes(String(name).toLowerCase()));
    const tokens = Array.from(new Set([...this.tokenizeText(query), ...conceptNames.map((name) => this.normalizeName(name))]));

    const conceptHits = concepts
      .map((concept) => {
        const match = this.scoreText([
          concept.name,
          concept.description,
          concept.sourceExcerpt,
          ...(concept.aliases || [])
        ], query, tokens);
        return { concept, score: match.score, matchedTerms: match.matchedTerms };
      })
      .filter((result) => result.score > 0)
      .sort((a, b) => b.score - a.score)
      .map((result) => ({ ...result.concept, matchedTerms: result.matchedTerms }));

    const sourceHits = sources
      .map((source) => {
        const match = this.scoreText([source.title, source.excerpt, source.path], query, tokens);
        return { source, score: match.score, matchedTerms: match.matchedTerms };
      })
      .filter((result) => result.score > 0)
      .sort((a, b) => b.score - a.score)
      .map((result) => ({ ...result.source, matchedTerms: result.matchedTerms }));

    const conceptIds = new Set(conceptHits.map((c) => c.id));
    const relationHits = relations.filter((r) => conceptIds.has(r.from) || conceptIds.has(r.to));

    if (options.mode === 'concepts') {
      return conceptHits;
    }

    return {
      concepts: conceptHits,
      sources: sourceHits,
      relations: relationHits,
      keywords: tokens,
      nextSteps: this.buildNextSteps({ concepts: conceptHits, sources: sourceHits, relations: relationHits })
    };
  }

  async getConcept(name) {
    const concepts = this.loadConcepts();
    return concepts.find((c) => this.normalizeName(c.name) === this.normalizeName(name));
  }

  async getRelated(conceptId) {
    const relations = this.loadRelations();
    const concepts = this.loadConcepts();
    return relations
      .filter((r) => r.from === conceptId || r.to === conceptId)
      .map((r) => {
        const otherId = r.from === conceptId ? r.to : r.from;
        const otherConcept = concepts.find((c) => c.id === otherId);
        return otherConcept ? {
          ...otherConcept,
          relationType: r.type,
          relationWeight: r.weight
        } : null;
      })
      .filter(Boolean);
  }

  buildNextSteps({ concepts, sources, relations }) {
    const nextSteps = [];
    if (sources.length === 0) {
      nextSteps.push('导入更多文档，让图谱结果不只来自单条输入。');
    }
    if (concepts.length > 0 && relations.length === 0) {
      nextSteps.push('运行自动关联，补出概念之间的关系边。');
    }
    if (concepts.length > 0) {
      nextSteps.push('围绕命中的核心概念生成 2 层子图，检查遗漏关系。');
    }
    if (sources.length > 1) {
      nextSteps.push('按命中的来源文档回看上下文，确认跨文档连接是否成立。');
    }
    return nextSteps;
  }

  async ask(question) {
    const keywords = question.match(/[\u4e00-\u9fa5]{2,}|[a-zA-Z]{3,}/g) || [];
    const aggregate = { concepts: [], sources: [], relations: [] };
    const seenConcepts = new Set();
    const seenSources = new Set();
    const seenRelations = new Set();

    for (const keyword of keywords) {
      const result = await this.search(keyword);
      for (const concept of result.concepts) {
        if (!seenConcepts.has(concept.id)) {
          seenConcepts.add(concept.id);
          aggregate.concepts.push(concept);
        }
      }
      for (const source of result.sources) {
        if (!seenSources.has(source.id)) {
          seenSources.add(source.id);
          aggregate.sources.push(source);
        }
      }
      for (const relation of result.relations) {
        if (!seenRelations.has(relation.id)) {
          seenRelations.add(relation.id);
          aggregate.relations.push(relation);
        }
      }
    }

    const answer = aggregate.concepts.length > 0
      ? `找到 ${aggregate.concepts.length} 个相关概念，覆盖 ${aggregate.sources.length} 个来源文档，并命中 ${aggregate.relations.length} 条关系。`
      : '未找到相关信息';

    return {
      answer,
      concepts: aggregate.concepts,
      sources: aggregate.sources,
      relations: aggregate.relations,
      nextSteps: this.buildNextSteps(aggregate)
    };
  }

  buildAnswerSummary(query, result) {
    const topConcepts = result.concepts.slice(0, 5).map((concept) => concept.name);
    const topSources = result.sources.slice(0, 5).map((source) => source.title);
    const lines = [`问题: ${query}`];
    if (topConcepts.length > 0) {
      lines.push(`命中概念: ${topConcepts.join('、')}`);
    }
    if (topSources.length > 0) {
      lines.push(`涉及文档: ${topSources.join('、')}`);
    }
    if (result.relations.length > 0) {
      lines.push(`相关关系数: ${result.relations.length}`);
    }
    return lines.join('\n');
  }

  async answer(query, options = {}) {
    const result = await this.search(query);
    const summary = this.buildAnswerSummary(query, result);

    if (options.format === 'html') {
      const conceptItems = result.concepts.slice(0, 12).map((concept) =>
        `<li><strong>${this.escapeHtml(concept.name)}</strong> <span style="color:#667">(${this.escapeHtml(concept.type)})</span></li>`
      ).join('');
      const sourceItems = result.sources.slice(0, 12).map((source) =>
        `<li><strong>${this.escapeHtml(source.title)}</strong><br><span style="color:#667">${this.escapeHtml(source.path)}</span></li>`
      ).join('');
      const nextStepItems = result.nextSteps.map((step) => `<li>${this.escapeHtml(step)}</li>`).join('');

      return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Knowledge Connector Answer</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; padding: 24px; color: #223; background: #f7f8fb; }
    .card { background: white; border: 1px solid #e3e6ee; border-radius: 16px; padding: 20px; margin-bottom: 16px; }
    h1, h2 { margin-top: 0; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    ul { padding-left: 18px; }
    code { background: #eef3ff; padding: 2px 6px; border-radius: 6px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Knowledge Connector Answer</h1>
    <p><strong>Query:</strong> ${this.escapeHtml(query)}</p>
    <pre>${this.escapeHtml(summary)}</pre>
  </div>
  <div class="grid">
    <div class="card">
      <h2>Matched Concepts</h2>
      <ul>${conceptItems || '<li>没有命中概念</li>'}</ul>
    </div>
    <div class="card">
      <h2>Matched Sources</h2>
      <ul>${sourceItems || '<li>没有命中文档</li>'}</ul>
    </div>
  </div>
  <div class="card">
    <h2>Next Steps</h2>
    <ul>${nextStepItems || '<li>继续导入更多文档扩展图谱。</li>'}</ul>
    <p>Tips: <code>kc map --concept &lt;概念&gt;</code> / <code>kc visualize --concept &lt;概念&gt;</code></p>
  </div>
</body>
</html>`;
    }

    return {
      query,
      summary,
      ...result
    };
  }

  async map(conceptName, depth = 2) {
    const center = await this.getConcept(conceptName);
    if (!center) {
      return null;
    }

    const concepts = this.loadConcepts();
    const relations = this.loadRelations();
    const relatedIds = new Set([center.id]);

    for (let i = 0; i < depth; i += 1) {
      const snapshot = new Set(relatedIds);
      for (const relation of relations) {
        if (snapshot.has(relation.from) || snapshot.has(relation.to)) {
          relatedIds.add(relation.from);
          relatedIds.add(relation.to);
        }
      }
    }

    const nodes = concepts.filter((concept) => relatedIds.has(concept.id));
    const edges = relations.filter((relation) => relatedIds.has(relation.from) && relatedIds.has(relation.to));

    return {
      center,
      nodes,
      edges,
      nextSteps: this.buildNextSteps({
        concepts: nodes,
        sources: this.loadSources().filter((source) => nodes.some((node) =>
          (node.sourceIds || []).includes(source.id) || (node.sources || []).includes(source.title)
        )),
        relations: edges
      })
    };
  }

  async visualize(options = {}) {
    const { format = 'html', concept, depth = 2 } = options;
    const graph = concept ? await this.map(concept, depth) : {
      center: null,
      nodes: this.loadConcepts(),
      edges: this.loadRelations(),
      nextSteps: this.buildNextSteps({
        concepts: this.loadConcepts(),
        sources: this.loadSources(),
        relations: this.loadRelations()
      })
    };

    const filteredConcepts = graph ? graph.nodes : [];
    const filteredRelations = graph ? graph.edges : [];

    if (format === 'json') {
      return JSON.stringify({
        center: graph.center,
        concepts: filteredConcepts,
        relations: filteredRelations,
        nextSteps: graph.nextSteps
      }, null, 2);
    }

    if (format === 'dot') {
      let dot = 'digraph KnowledgeGraph {\n';
      dot += '  rankdir=LR;\n';
      dot += '  node [shape=box, style=rounded];\n\n';
      for (const conceptNode of filteredConcepts) {
        dot += `  "${this.escapeDotLabel(conceptNode.id)}" [label="${this.escapeDotLabel(conceptNode.name)}"];\n`;
      }
      dot += '\n';
      for (const relation of filteredRelations) {
        dot += `  "${this.escapeDotLabel(relation.from)}" -> "${this.escapeDotLabel(relation.to)}" [label="${this.escapeDotLabel(relation.type)}"];\n`;
      }
      dot += '}';
      return dot;
    }

    const summaryItems = graph.nextSteps.map((item) => `<li>${this.escapeHtml(item)}</li>`).join('');
    const centerSummary = graph.center ? ` | 中心概念: ${this.escapeHtml(graph.center.name)}` : '';
    const graphNodesJson = this.safeJsonForScript(filteredConcepts.map((conceptNode) => ({
      id: conceptNode.id,
      label: conceptNode.name,
      title: conceptNode.description || conceptNode.sourceExcerpt || conceptNode.name,
      color: conceptNode.type === 'tech' ? '#d7ebff' : '#eef2f7'
    })));
    const graphEdgesJson = this.safeJsonForScript(filteredRelations.map((relation) => ({
      from: relation.from,
      to: relation.to,
      label: relation.type,
      arrows: 'to'
    })));
    return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>知识图谱</title>
  <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    body { margin: 0; padding: 20px; font-family: Arial, sans-serif; color: #223; }
    .layout { display: grid; grid-template-columns: 1fr 320px; gap: 16px; }
    #graph { width: 100%; height: 640px; border: 1px solid #ddd; border-radius: 12px; }
    .panel { border: 1px solid #ddd; border-radius: 12px; padding: 16px; background: #fafafa; }
    .stats { margin: 10px 0 16px; color: #666; }
    h1, h2 { margin: 0 0 12px; }
    ul { padding-left: 18px; }
    code { background: #eef3ff; padding: 2px 6px; border-radius: 6px; }
  </style>
</head>
<body>
  <h1>知识图谱</h1>
  <div class="stats">概念: ${filteredConcepts.length} | 关系: ${filteredRelations.length}${centerSummary}</div>
  <div class="layout">
    <div id="graph"></div>
    <div class="panel">
      <h2>下一步建议</h2>
      <ul>${summaryItems || '<li>继续导入文档，扩展图谱范围。</li>'}</ul>
      <h2>使用提示</h2>
      <ul>
        <li>用 <code>kc search &lt;关键词&gt;</code> 做跨文档搜索</li>
        <li>用 <code>kc map --concept &lt;概念&gt;</code> 看可操作子图</li>
        <li>用 <code>kc import-docs --dir &lt;目录&gt;</code> 批量导入</li>
      </ul>
    </div>
  </div>
  <script>
    const nodes = new vis.DataSet(${graphNodesJson});
    const edges = new vis.DataSet(${graphEdgesJson});
    const network = new vis.Network(
      document.getElementById('graph'),
      { nodes, edges },
      {
        nodes: { shape: 'box', margin: 10, font: { size: 14 } },
        edges: { font: { size: 12 }, smooth: { type: 'continuous' } },
        physics: { stabilization: false }
      }
    );
  </script>
</body>
</html>`;
  }

  findExecutable(commandName) {
    const pathDirs = String(process.env.PATH || '').split(path.delimiter).filter(Boolean);
    const names = process.platform === 'win32'
      ? [commandName, `${commandName}.cmd`, `${commandName}.exe`]
      : [commandName];

    for (const dir of pathDirs) {
      for (const name of names) {
        const candidate = path.join(dir, name);
        try {
          fs.accessSync(candidate, fs.constants.X_OK);
          return candidate;
        } catch {
          // Keep looking through PATH.
        }
      }
    }
    return null;
  }

  doctor() {
    const packageRoot = path.join(__dirname, '..');
    const packageFile = path.join(packageRoot, 'package.json');
    const binFile = path.join(packageRoot, 'bin', 'cli.js');
    const checks = [];
    const addCheck = (name, ok, detail, severity = 'error') => {
      checks.push({ name, ok: Boolean(ok), detail, severity });
    };

    addCheck('data directory exists', fs.existsSync(this.dataDir), this.dataDir);
    if (this.initError) {
      addCheck('data store initialized', false, this.initError.message);
    } else {
      addCheck('data store initialized', true, this.dataDir);
    }
    try {
      fs.accessSync(this.dataDir, fs.constants.W_OK);
      addCheck('data directory writable', true, this.dataDir);
    } catch (error) {
      addCheck('data directory writable', false, error.message);
    }

    for (const file of [this.conceptsFile, this.relationsFile, this.sourcesFile]) {
      try {
        const data = JSON.parse(fs.readFileSync(file, 'utf-8'));
        addCheck(`${path.basename(file)} is readable JSON array`, Array.isArray(data), file);
      } catch (error) {
        addCheck(`${path.basename(file)} is readable JSON array`, false, error.message);
      }
    }

    let packageData = null;
    try {
      packageData = JSON.parse(fs.readFileSync(packageFile, 'utf-8'));
      addCheck('package.json readable', true, packageFile);
    } catch (error) {
      addCheck('package.json readable', false, error.message);
    }

    addCheck('CLI entry file exists', fs.existsSync(binFile), binFile);
    if (packageData) {
      addCheck('kc bin declared', Boolean(packageData.bin && packageData.bin.kc), packageData.bin && packageData.bin.kc ? packageData.bin.kc : 'missing');
      addCheck('repository URL configured', Boolean(packageData.repository && packageData.repository.url), packageData.repository && packageData.repository.url ? packageData.repository.url : 'missing', 'warning');
    }

    const kcExecutable = this.findExecutable('kc');
    addCheck('kc command on PATH', Boolean(kcExecutable), kcExecutable || 'not found; run through installed package or node bin/cli.js', 'warning');

    const ok = checks.every((check) => check.ok || check.severity === 'warning');
    return {
      ok,
      dataDir: this.dataDir,
      packageRoot,
      version: packageData ? packageData.version : null,
      checks
    };
  }

  async getStats() {
    const concepts = this.loadConcepts();
    const relations = this.loadRelations();
    const sources = this.loadSources();
    return {
      conceptCount: concepts.length,
      relationCount: relations.length,
      sourceCount: sources.length,
      typeCount: new Set(concepts.map((c) => c.type).filter(Boolean)).size,
      dataSize: this.getDataSize()
    };
  }

  getDataSize() {
    try {
      const total = [this.conceptsFile, this.relationsFile, this.sourcesFile]
        .map((file) => fs.statSync(file).size)
        .reduce((sum, size) => sum + size, 0);
      if (total < 1024) return `${total} B`;
      if (total < 1024 * 1024) return `${(total / 1024).toFixed(2)} KB`;
      return `${(total / (1024 * 1024)).toFixed(2)} MB`;
    } catch {
      return '0 B';
    }
  }

  async export() {
    return {
      concepts: this.loadConcepts(),
      relations: this.loadRelations(),
      sources: this.loadSources(),
      exportedAt: new Date().toISOString()
    };
  }

  async import(data) {
    if (data.concepts) {
      this.saveConceptsData(data.concepts);
    }
    if (data.relations) {
      this.saveRelationsData(data.relations);
    }
    if (data.sources) {
      this.saveSourcesData(data.sources);
    }
  }

  async clear() {
    this.saveConceptsData([]);
    this.saveRelationsData([]);
    this.saveSourcesData([]);
  }

  async recommend(conceptName, limit = 5) {
    const concept = await this.getConcept(conceptName);
    if (!concept) {
      return [];
    }

    return (await this.getRelated(concept.id))
      .sort((a, b) => b.relationWeight - a.relationWeight)
      .slice(0, limit)
      .map((related) => ({
        id: related.id,
        name: related.name,
        type: related.type,
        score: related.relationWeight,
        reason: `与 ${conceptName} 存在“${related.relationType}”关系`
      }));
  }
}

module.exports = KnowledgeConnector;
