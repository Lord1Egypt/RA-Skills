class Analyzer {
  analyzeFields(data) {
    const fields = {};
    
    // 遍历数据对象的所有属性
    for (const key in data) {
      if (data.hasOwnProperty(key)) {
        const value = data[key];
        // 确定字段类型
        fields[key] = this.getType(value);
      }
    }
    
    return fields;
  }

  getType(value) {
    if (value === null) {
      return 'null';
    } else if (Array.isArray(value)) {
      return 'array';
    } else if (typeof value === 'object') {
      return 'object';
    } else {
      return typeof value;
    }
  }
}

module.exports = Analyzer;