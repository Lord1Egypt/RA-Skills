const path = require('path');
const fs = require('fs');

class LocalVectorStore {
  constructor() {
    this.config = {
      dimension: parseInt(process.env.VECTOR_DIMENSION || '384', 10),
      storePath: process.env.STORE_PATH || '/tmp/vector-store',
      similarityThreshold: parseFloat(process.env.SIMILARITY_THRESHOLD || '0.5')
    };
    this.documents = new Map();
    this.vectors = new Map();
  }

  async create(options = {}) {
    const { dimension = this.config.dimension, storePath = this.config.storePath } = options;

    this.config.dimension = dimension;
    this.config.storePath = storePath;

    if (!fs.existsSync(storePath)) {
      fs.mkdirSync(storePath, { recursive: true });
    }

    return this;
  }

  async index(doc) {
    const { id, content, metadata = {} } = doc;

    if (!id || !content) {
      throw new Error('Document must have id and content');
    }

    const vector = this._generateVector(content);
    this.documents.set(id, { content, metadata, timestamp: Date.now() });
    this.vectors.set(id, vector);

    await this._persistDocument(id, doc, vector);
    return { id, indexed: true };
  }

  async indexBatch(docs) {
    const results = [];
    for (const doc of docs) {
      try {
        results.push(await this.index(doc));
      } catch (err) {
        results.push({ id: doc.id, error: err.message });
      }
    }
    return results;
  }

  async search(options = {}) {
    const { query, topK = 5, threshold = this.config.similarityThreshold } = options;

    if (!query) {
      throw new Error('Search query is required');
    }

    const startTime = Date.now();
    const queryVector = this._generateVector(query);
    const similarities = [];

    for (const [docId, docVector] of this.vectors.entries()) {
      const similarity = this._cosineSimilarity(queryVector, docVector);
      if (similarity >= threshold) {
        similarities.push({
          id: docId,
          similarity,
          ...this.documents.get(docId)
        });
      }
    }

    const results = similarities
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, topK);

    return {
      query,
      results,
      searchTime: Date.now() - startTime,
      totalMatches: similarities.length
    };
  }

  async delete(id) {
    this.documents.delete(id);
    this.vectors.delete(id);
    const filePath = path.join(this.config.storePath, `${id}.json`);
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }
    return { id, deleted: true };
  }

  async clear() {
    this.documents.clear();
    this.vectors.clear();
    const files = fs.readdirSync(this.config.storePath);
    for (const file of files) {
      fs.unlinkSync(path.join(this.config.storePath, file));
    }
    return { cleared: true };
  }

  async getStats() {
    return {
      totalDocuments: this.documents.size,
      storePath: this.config.storePath,
      dimension: this.config.dimension,
      threshold: this.config.similarityThreshold
    };
  }

  _generateVector(text) {
    const hash = this._simpleHash(text);
    const vector = [];
    for (let i = 0; i < this.config.dimension; i++) {
      vector.push(Math.sin(hash + i) * 0.5 + 0.5);
    }
    return vector;
  }

  _cosineSimilarity(vec1, vec2) {
    if (vec1.length !== vec2.length) return 0;

    let dotProduct = 0;
    let mag1 = 0;
    let mag2 = 0;

    for (let i = 0; i < vec1.length; i++) {
      dotProduct += vec1[i] * vec2[i];
      mag1 += vec1[i] * vec1[i];
      mag2 += vec2[i] * vec2[i];
    }

    mag1 = Math.sqrt(mag1);
    mag2 = Math.sqrt(mag2);

    if (mag1 === 0 || mag2 === 0) return 0;
    return dotProduct / (mag1 * mag2);
  }

  _simpleHash(text) {
    let hash = 0;
    for (let i = 0; i < text.length; i++) {
      const char = text.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash;
    }
    return Math.abs(hash);
  }

  async _persistDocument(id, doc, vector) {
    const filePath = path.join(this.config.storePath, `${id}.json`);
    const data = { ...doc, vector, timestamp: Date.now() };
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
  }

  async main() {
    console.log('Local Vector Store initialized');
    return { status: 'ok', version: '1.0.0', dimension: this.config.dimension };
  }
}

module.exports = new LocalVectorStore();
