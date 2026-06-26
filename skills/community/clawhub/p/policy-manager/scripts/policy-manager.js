#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const POLICIES_DIR = '/Users/wuaihua/workspaces/insurance-clerk/policies';

// API 配置（后续由用户配置真实端点）
const API_CONFIG = {
  baseUrl: process.env.POLICY_API_URL || '',  // 例如：https://api.example.com
  endpoints: {
    getPolicyTemplate: '/api/policy/template',  // 获取保单模板
  },
  timeout: 5000
};

// 确保目录存在
if (!fs.existsSync(POLICIES_DIR)) {
  fs.mkdirSync(POLICIES_DIR, { recursive: true });
}

// HTTP 请求封装
function httpRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    
    const req = lib.request(url, {
      method: options.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      timeout: API_CONFIG.timeout
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data) });
        } catch (e) {
          reject(new Error(`响应解析失败：${e.message}`));
        }
      });
    });
    
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('请求超时'));
    });
    
    if (options.body) {
      req.write(JSON.stringify(options.body));
    }
    req.end();
  });
}

// 获取保单模板（调用 API 或 Mock）
async function getPolicyTemplate(insuranceCode, productCode) {
  // 如果配置了 API 端点，调用真实 API
  if (API_CONFIG.baseUrl) {
    try {
      const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.getPolicyTemplate}?insuranceCode=${insuranceCode}&productCode=${productCode}`;
      const response = await httpRequest(url);
      if (response.status === 200) {
        return response.data;
      } else {
        throw new Error(`API 返回错误状态：${response.status}`);
      }
    } catch (error) {
      console.error(`API 调用失败：${error.message}，使用 Mock 模板`);
    }
  }
  
  // 从 mock-api.json 读取模板（本地 Mock）
  try {
    const mockApiPath = '/Users/wuaihua/workspaces/insurance-clerk/mock-api.json';
    const mockData = JSON.parse(fs.readFileSync(mockApiPath, 'utf-8'));
    
    // 深拷贝模板，避免修改原始数据
    const template = JSON.parse(JSON.stringify(mockData.policyTemplate));
    
    // 填充基本信息
    template.productCode = productCode;
    template.productInsuranceCode = insuranceCode;
    
    // 从 mock 数据中获取产品名称
    const productList = mockData.productList[insuranceCode] || [];
    const product = productList.find(p => p.code === productCode);
    if (product) {
      template.productName = product.name;
    }
    
    return template;
  } catch (error) {
    console.error(`读取 Mock 数据失败：${error.message}`);
    // 返回最小可用模板
    return {
      productCode: productCode,
      productInsuranceCode: insuranceCode,
      productName: "",
      policyStatus: "DRAFT",
      policyHolder: {
        type: "PERSON",
        role: "HOLDER",
        certType: "ID_CARD",
        extraInfo: {},
        policyCustomerPerson: {
          extraInfo: {}
        }
      },
      policyInsurantList: [],
      insuredPersonList: [],
      insuredObjList: [],
      extraInfo: {}
    };
  }
}

function getFilepath(taskNo) {
  return path.join(POLICIES_DIR, `${taskNo}.json`);
}

async function createPolicy(args) {
  const { taskNo, insuranceCode, productCode } = args;
  const filepath = getFilepath(taskNo);

  // 检查文件是否已存在
  if (fs.existsSync(filepath)) {
    return { success: false, message: "保单文件已存在" };
  }

  try {
    const template = await getPolicyTemplate(insuranceCode, productCode);
    const policy = {
      ...template,
      taskNo,
      insuranceCode,
      productCode,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    fs.writeFileSync(filepath, JSON.stringify(policy, null, 2));
    return { success: true, message: "保单文件创建成功" };
  } catch (error) {
    return { success: false, message: `创建失败：${error.message}` };
  }
}

function updatePolicy(args) {
  const { taskNo, updateType, data } = args;
  const filepath = getFilepath(taskNo);

  // 检查文件是否存在
  if (!fs.existsSync(filepath)) {
    return { success: false, message: "保单文件不存在" };
  }

  try {
    const policy = JSON.parse(fs.readFileSync(filepath, 'utf-8'));

    // 根据 updateType 更新对应字段
    if (updateType === 'materials') {
      policy.materials = data;
    } else if (updateType === 'extractedData') {
      policy.extractedData = data;
    } else {
      policy[updateType] = data;
    }

    policy.updatedAt = new Date().toISOString();
    fs.writeFileSync(filepath, JSON.stringify(policy, null, 2));
    return { success: true, message: "保单文件更新成功" };
  } catch (error) {
    return { success: false, message: `更新失败：${error.message}` };
  }
}

function readPolicy(args) {
  const { taskNo } = args;
  const filepath = getFilepath(taskNo);

  if (!fs.existsSync(filepath)) {
    return { success: false, message: "保单文件不存在" };
  }

  try {
    const policy = JSON.parse(fs.readFileSync(filepath, 'utf-8'));
    return { success: true, data: policy };
  } catch (error) {
    return { success: false, message: `读取失败：${error.message}` };
  }
}

// CLI 入口
const action = process.argv[2];
const args = {};
const argv = process.argv.slice(3);

for (let i = 0; i < argv.length; i++) {
  if (argv[i].startsWith('--')) {
    const key = argv[i].slice(2);
    // 检查下一个参数是否是值（不是以 -- 开头）
    if (i + 1 < argv.length && !argv[i + 1].startsWith('--')) {
      args[key] = argv[i + 1];
      i++; // 跳过下一个参数
    } else {
      args[key] = true;
    }
  }
}

// 解析 JSON 数据
if (args.data) {
  try {
    args.data = JSON.parse(args.data);
  } catch (e) {
    console.log(JSON.stringify({ success: false, message: 'data 参数格式错误' }));
    process.exit(1);
  }
}

async function main() {
  let result;
  switch (action) {
    case 'create':
      result = await createPolicy(args);
      break;
    case 'update':
      result = updatePolicy(args);
      break;
    case 'read':
      result = readPolicy(args);
      break;
    default:
      result = { success: false, message: '未知操作，支持：create, update, read' };
  }
  console.log(JSON.stringify(result));
}

main().catch(err => {
  console.log(JSON.stringify({ success: false, message: `执行错误：${err.message}` }));
});
