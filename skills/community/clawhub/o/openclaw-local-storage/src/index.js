const fs = require('fs');
const path = require('path');
const Storage = require('./storage');
const Parser = require('./parser');
const Analyzer = require('./analyzer');

class OpenClawLocalStorage {
  constructor() {
    this.storage = new Storage();
    this.parser = new Parser();
    this.analyzer = new Analyzer();
    this.isInitialized = false;
  }

  async processCommand(command) {
    if (!this.isInitialized) {
      return await this.initialize(command);
    }

    const parsed = this.parser.parseCommand(command);
    if (!parsed) {
      return '无法解析命令，请使用正确的格式';
    }

    switch (parsed.action) {
      case 'add':
        return await this.storage.add(parsed.data);
      case 'query':
        return await this.storage.query(parsed.conditions);
      case 'update':
        return await this.storage.update(parsed.conditions, parsed.data);
      case 'delete':
        return await this.storage.delete(parsed.conditions);
      default:
        return '不支持的操作类型';
    }
  }

  async initialize(command) {
    // 提取首次存储的数据
    const dataMatch = command.match(/存储一条.*：(.*)/);
    if (!dataMatch) {
      return '请提供要存储的数据，格式为：存储一条[类型]信息：{"字段1": "值1", "字段2": "值2"}';
    }

    try {
      const data = JSON.parse(dataMatch[1]);
      const fields = this.analyzer.analyzeFields(data);
      
      // 初始化存储
      await this.storage.init(fields);
      await this.storage.add(data);
      
      this.isInitialized = true;
      return `初始化成功！分析出以下字段：${Object.keys(fields).join('、')}`;
    } catch (error) {
      return '数据格式错误，请确保输入的是有效的JSON格式';
    }
  }
}

module.exports = OpenClawLocalStorage;