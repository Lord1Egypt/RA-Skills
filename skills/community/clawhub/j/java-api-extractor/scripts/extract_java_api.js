#!/usr/bin/env node
/**
 * 从 Java Spring Boot 项目中提取 Controller 层接口定义为 JSON 数据
 */

const fs = require('fs');
const path = require('path');

const TEMPLATE_FILE = 'D:\\working\\接口文档数据模版.json';
const API_DOCS_DIR = 'D:\\working\\coding\\api-docs';

const JAVA_TO_JSON_TYPE = {
  'String': 'string', 'Integer': 'integer', 'int': 'integer',
  'Long': 'integer', 'long': 'integer',
  'Boolean': 'boolean', 'boolean': 'boolean',
  'Double': 'number', 'double': 'number',
  'Float': 'number', 'float': 'number',
  'Date': 'string', 'LocalDateTime': 'string', 'LocalDate': 'string',
  'List': 'array', 'Set': 'array', 'Array': 'array',
  'Map': 'object', 'Object': 'object',
};

const MAPPING_TO_METHOD = {
  'GetMapping': 'GET', 'PostMapping': 'POST', 'PutMapping': 'PUT',
  'DeleteMapping': 'DELETE', 'PatchMapping': 'PATCH', 'RequestMapping': 'GET',
};

function findControllers(projectPath, packageFilter = null) {
  const controllers = [];
  const srcPath = path.join(projectPath, 'src', 'main', 'java');
  if (!fs.existsSync(srcPath)) return controllers;
  
  function walkDir(dir) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      if (stat.isDirectory()) {
        walkDir(filePath);
      } else if (file.endsWith('.java')) {
        if (packageFilter && !filePath.includes(packageFilter.replace(/\./g, path.sep))) continue;
        if (isController(filePath)) controllers.push(filePath);
      }
    }
  }
  walkDir(srcPath);
  return controllers;
}

function isController(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    return content.includes('@RestController') || content.includes('@Controller');
  } catch (e) { return false; }
}

function extractClassPath(content) {
  const patterns = [
    /@RequestMapping\s*\(\s*"([^"]+)"\s*\)/,
    /@RequestMapping\s*\(\s*value\s*=\s*"([^"]+)"\s*\)/,
  ];
  for (const pattern of patterns) {
    const match = content.match(pattern);
    if (match) return match[1];
  }
  return '';
}

function extractClassDescription(content) {
  const patterns = [/@Tag\s*\(\s*name\s*=\s*"([^"]+)"/, /@Api\s*\(\s*description\s*=\s*"([^"]+)"/];
  for (const pattern of patterns) {
    const match = content.match(pattern);
    if (match) return match[1];
  }
  return '';
}

function findMethods(content) {
  const methods = [];
  const pattern = /@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping|RequestMapping)(?:\s*\(\s*(?:value\s*=\s*)?"([^"]*)"\s*\))?\s*[\r\n]*\s*(public|private|protected)\s+(\w+(?:<[^>]+>)?)\s+(\w+)\s*\(([^)]*)\)/g;
  
  let match;
  while ((match = pattern.exec(content)) !== null) {
    const annotation = match[1];
    const pathValue = match[2] || '';
    const returnType = match[4];
    const methodName = match[5];
    const startIndex = match.index;
    
    // 找到方法体
    const openBrace = content.indexOf('{', startIndex);
    if (openBrace === -1) continue;
    
    let braceCount = 1, endIndex = openBrace + 1;
    while (braceCount > 0 && endIndex < content.length) {
      if (content[endIndex] === '{') braceCount++;
      else if (content[endIndex] === '}') braceCount--;
      endIndex++;
    }
    
    const methodBody = content.substring(startIndex, endIndex);
    // 使用对象包装，因为字符串不能附加属性
    methods.push({
      body: methodBody,
      annotation: annotation,
      pathValue: pathValue,
      returnType: returnType,
      methodName: methodName
    });
  }
  return methods;
}

function extractApis(controllerFile, projectPath) {
  const apis = [];
  try {
    const content = fs.readFileSync(controllerFile, 'utf-8');
    const classPath = extractClassPath(content);
    const classDescription = extractClassDescription(content);
    const methods = findMethods(content);
    
    for (const method of methods) {
      const apiDef = parseMethod(method, classPath, classDescription, controllerFile, projectPath);
      if (apiDef) apis.push(apiDef);
    }
  } catch (e) {
    console.log(`❌ 读取文件失败 ${controllerFile}: ${e.message}`);
  }
  return apis;
}

function parseMethod(methodObj, classPath, classDescription, controllerFile, projectPath) {
  const annotation = methodObj.annotation || '';
  const returnType = methodObj.returnType || 'void';
  const pathValue = methodObj.pathValue || '';
  const methodName = methodObj.methodName || 'unknown';
  const methodBlock = methodObj.body;
  
  const apiDef = {
    name: '', path: '', method: MAPPING_TO_METHOD[annotation] || 'GET', description: '',
    requestParams: [],
    responseSchema: { type: 'object', properties: { code: { type: 'integer', description: '状态码' }, msg: { type: 'string', description: '响应消息' }, data: { type: 'object', description: '返回数据' } } }
  };
  
  // 提取路径
  const methodPath = pathValue;
  
  if (classPath && methodPath) {
    apiDef.path = `${classPath.replace(/\/$/, '')}/${methodPath.replace(/^\//, '')}`;
  } else if (classPath) {
    apiDef.path = classPath;
  } else {
    apiDef.path = methodPath || '/';
  }
  apiDef.path = apiDef.path.replace(/\/\//g, '/');
  
  // 提取描述
  const descMatch = methodBlock.match(/@ApiOperation\s*\([^)]*value\s*=\s*"([^"]+)"|@Operation\s*\([^)]*summary\s*=\s*"([^"]+)"/);
  apiDef.description = descMatch ? (descMatch[1] || descMatch[2]) : camelToChinese(methodName);
  apiDef.name = apiDef.description.split('。')[0].split(',')[0].trim().substring(0, 50);
  
  // 提取参数
  apiDef.requestParams = extractParams(methodBlock, projectPath);
  
  // 提取响应 Schema
  apiDef.responseSchema = extractResponseSchema(returnType, projectPath);
  
  return apiDef;
}

function extractParams(methodBlock, projectPath) {
  const params = [];
  
  // @PathVariable
  let match;
  const pathVarPattern = /@PathVariable\s*(?:\(\s*(?:value\s*=\s*)?"([^"]+)"\s*\))?\s*(\w+)\s+(\w+)/g;
  while ((match = pathVarPattern.exec(methodBlock)) !== null) {
    params.push({ name: match[1] || match[3], type: match[2], required: true, description: `路径参数：${match[1] || match[3]}` });
  }
  
  // @RequestParam
  const paramPattern = /@RequestParam\s*(?:\([^)]*value\s*=\s*"([^"]+)"[^)]*\))?[^)]*(?:required\s*=\s*(true|false))?[^)]*\)\s*(\w+)\s+(\w+)/g;
  while ((match = paramPattern.exec(methodBlock)) !== null) {
    params.push({ name: match[1] || match[4], type: match[3], required: match[2] !== 'false', description: `查询参数：${match[1] || match[4]}` });
  }
  
  // @RequestBody
  if (methodBlock.includes('@RequestBody')) {
    const bodyMatch = methodBlock.match(/@RequestBody\s+(?:@Valid\s+)?(\w+)\s+\w+/);
    if (bodyMatch) {
      params.push(...extractDtoFields(bodyMatch[1], projectPath));
    }
  }
  
  return params;
}

function extractDtoFields(dtoType, projectPath) {
  const fields = [];
  const srcPath = path.join(projectPath, 'src', 'main', 'java');
  if (!fs.existsSync(srcPath)) return fields;
  
  function findClassFile(dir, className) {
    try {
      for (const file of fs.readdirSync(dir)) {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat.isDirectory()) {
          const result = findClassFile(filePath, className);
          if (result) return result;
        } else if (file === className + '.java') {
          return filePath;
        }
      }
    } catch (e) {}
    return null;
  }
  
  const classFile = findClassFile(srcPath, dtoType);
  if (!classFile) return fields;
  
  try {
    const content = fs.readFileSync(classFile, 'utf-8');
    const fieldPattern = /(?:private|public|protected)\s+(?:static\s+final\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)\s*;/g;
    let match;
    while ((match = fieldPattern.exec(content)) !== null) {
      const fieldType = match[1], fieldName = match[2];
      if (fieldName === 'serialVersionUID') continue;
      
      let description = fieldName;
      const fieldIndex = content.indexOf(fieldName);
      if (fieldIndex > 0) {
        const beforeField = content.substring(Math.max(0, fieldIndex - 150), fieldIndex);
        const commentMatch = beforeField.match(/\/\*\*\s*\*\s*([^\*\n]+)/);
        if (commentMatch) description = commentMatch[1].trim();
      }
      
      fields.push({ name: fieldName, type: JAVA_TO_JSON_TYPE[fieldType] || 'string', description });
    }
  } catch (e) {}
  
  return fields;
}

function extractResponseSchema(returnType, projectPath) {
  const schema = {
    type: 'object',
    properties: {
      code: { type: 'integer', description: '状态码' },
      msg: { type: 'string', description: '响应消息' },
      data: { type: 'object', description: '返回数据' }
    }
  };
  
  if (!returnType) return schema;
  
  let isArray = false, innerType = null;
  const genericMatch = returnType.match(/(\w+)<(\w+)>/);
  if (genericMatch) {
    const wrapperType = genericMatch[1];
    innerType = genericMatch[2];
    if (['List', 'Set', 'Array', 'PageInfo'].includes(wrapperType)) {
      isArray = true;
      returnType = innerType;
    }
  }
  
  const baseTypes = ['void', 'Void', 'String', 'Integer', 'int', 'Long', 'long', 'Boolean', 'boolean', 'Double', 'double', 'Float', 'float'];
  
  if (baseTypes.includes(returnType)) {
    if (returnType === 'void' || returnType === 'Void') {
      schema.properties.data = { type: 'null', description: '无返回数据' };
    } else {
      schema.properties.data = { type: JAVA_TO_JSON_TYPE[returnType] || 'string', description: `返回数据：${returnType}` };
    }
  } else if (isArray) {
    const fields = extractDtoFields(returnType, projectPath);
    const itemsProps = {};
    fields.forEach(f => { itemsProps[f.name] = { type: f.type, description: f.description }; });
    schema.properties.data = {
      type: 'array',
      description: `返回数据：${returnType} 数组`,
      items: { type: 'object', properties: itemsProps }
    };
  } else {
    const fields = extractDtoFields(returnType, projectPath);
    const dataProps = {};
    fields.forEach(f => { dataProps[f.name] = { type: f.type, description: f.description }; });
    schema.properties.data = {
      type: 'object',
      description: `返回数据：${returnType}`,
      properties: dataProps
    };
  }
  
  return schema;
}

function camelToChinese(name) {
  const map = { 'get': '获取', 'create': '创建', 'add': '添加', 'save': '保存', 'update': '更新', 'delete': '删除', 'remove': '移除', 'list': '列表', 'query': '查询' };
  for (const [en, zh] of Object.entries(map)) {
    if (name.toLowerCase().startsWith(en)) return `${zh}${name.substring(en.length)}`;
  }
  return name;
}

function loadTemplate() {
  if (fs.existsSync(TEMPLATE_FILE)) return JSON.parse(fs.readFileSync(TEMPLATE_FILE, 'utf-8'));
  return { name: '', path: '', method: 'GET', description: '', requestParams: [], responseSchema: { type: 'object', properties: {} } };
}

function apiDefToJson(apiDef, template) {
  return {
    name: apiDef.name || template.name,
    path: apiDef.path || template.path,
    method: apiDef.method || template.method,
    description: apiDef.description || template.description,
    requestParams: apiDef.requestParams.map(p => ({ name: p.name, type: p.type, required: p.required, description: p.description })),
    responseSchema: apiDef.responseSchema
  };
}

function main() {
  const args = process.argv.slice(2);
  const argMap = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].substring(2);
      argMap[key] = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
    }
  }
  
  const { project, output, package: packageFilter, verbose, noBackup } = argMap;
  
  if (!project) { console.log('❌ 必须指定 --project'); process.exit(1); }
  if (!fs.existsSync(project)) { console.log(`❌ 项目不存在：${project}`); process.exit(1); }
  
  console.log('🔍 开始提取 Java 项目接口定义...');
  console.log(`   项目路径：${project}`);
  
  const controllers = findControllers(project, packageFilter);
  if (!controllers.length) { console.log('❌ 未找到 Controller'); process.exit(1); }
  console.log(`📂 找到 ${controllers.length} 个 Controller 类`);
  
  const allApis = [];
  const template = loadTemplate();
  
  for (const controller of controllers) {
    if (verbose) console.log(`\n📄 处理：${path.basename(controller)}`);
    const apis = extractApis(controller, project);
    for (const api of apis) {
      allApis.push(apiDefToJson(api, template));
      if (verbose) console.log(`  ✓ ${api.method} ${api.path}`);
    }
  }
  
  console.log(`\n✅ 共提取 ${allApis.length} 个接口定义`);
  
  if (output) {
    fs.writeFileSync(output, JSON.stringify(allApis, null, 2), 'utf-8');
    console.log(`📄 已保存到：${output}`);
  } else {
    console.log(JSON.stringify(allApis, null, 2));
  }
  
  if (!noBackup) {
    try {
      const apiDocsDir = path.join(API_DOCS_DIR);
      if (!fs.existsSync(apiDocsDir)) fs.mkdirSync(apiDocsDir, { recursive: true });
      const ts = new Date().toISOString().replace(/[-:T.]/g, '').substring(0, 14);
      const backupPath = path.join(apiDocsDir, `api-definitions-${ts}.json`);
      fs.writeFileSync(backupPath, JSON.stringify(allApis, null, 2), 'utf-8');
      console.log(`💾 已备份到：${backupPath}`);
    } catch (e) { console.log(`⚠️ 备份失败：${e.message}`); }
  }
}

main();
