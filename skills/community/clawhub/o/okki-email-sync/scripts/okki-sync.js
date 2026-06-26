/**
 * OKKI Sync Module - 邮件/报价单自动写入 OKKI 跟进记录
 * 
 * 功能:
 * 1. matchCustomer(email) - 域名匹配（含公共域黑名单）+ 向量搜索回退
 * 2. createEmailTrail(companyId, emailData) - 创建邮件类型跟进记录（trail_type=102）
 * 3. createQuotationTrail(companyId, quotationData) - 创建报价单类型跟进记录（trail_type=101）
 * 4. 去重检查：以邮件 UID 为 key，维护 /tmp/okki-sync-processed.json
 * 5. 匹配失败时写入 /tmp/okki-unmatched-emails.log
 */

const { execFile } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

// ==================== 配置 ====================
const CONFIG = {
  // OKKI CLI 路径（可通过环境变量覆盖）
  okkiCliPath: process.env.OKKI_CLI_PATH || path.join(__dirname, '../../xiaoman-okki/api/okki.py'),
  
  // 客户向量搜索脚本路径（可通过环境变量覆盖）
  customerSearchScript: process.env.VECTOR_SEARCH_PATH || path.join(__dirname, '../../vector_store/search-customers.py'),
  
  // Python 虚拟环境路径（可通过环境变量覆盖）
  pythonVenv: process.env.PYTHON_VENV_PATH || 'python3',
  
  // 公共域名黑名单
  publicDomains: [
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
    'qq.com', '163.com', '126.com', 'sina.com', 'sohu.com',
    'icloud.com', 'me.com', 'mac.com', 'live.com', 'msn.com'
  ],
  
  // 去重记录文件（可通过环境变量覆盖）
  processedFile: process.env.OKKI_SYNC_RECORD_FILE || path.join(os.tmpdir(), 'okki-sync-processed.json'),
  
  // 未匹配日志文件
  unmatchedLog: path.join(os.tmpdir(), 'okki-unmatched-emails.log'),
  
  // Trail 类型枚举
  TRAIL_TYPE: {
    QUOTATION: 101,  // 快速记录
    EMAIL: 102,      // 邮件
    PHONE: 103,      // 电话
    MEETING: 104,    // 会面
    SOCIAL: 105      // 社交平台
  }
};

// ==================== 工具函数 ====================

/**
 * 执行 Python 脚本
 */
function execPython(scriptPath, args = [], options = {}) {
  return new Promise((resolve, reject) => {
    // 使用配置的 Python 路径（可能是 venv 或系统 Python）
    const pythonPath = CONFIG.pythonVenv;
    
    const fullArgs = [scriptPath, ...args];
    
    execFile(pythonPath, fullArgs, {
      timeout: options.timeout || 10000,
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    }, (error, stdout, stderr) => {
      if (error) {
        reject(new Error(`Python 执行失败：${error.message}\n${stderr}`));
        return;
      }
      
      try {
        const result = JSON.parse(stdout);
        resolve(result);
      } catch (e) {
        resolve({ raw: stdout, stderr });
      }
    });
  });
}

/**
 * 执行 OKKI CLI 命令
 * 注意：--json 等全局标志必须放在子命令之前
 */
function execOkkiCli(args = [], options = {}) {
  return new Promise((resolve, reject) => {
    // --json 是全局标志，需要放在子命令之前
    const fullArgs = [CONFIG.okkiCliPath, '--json', ...args];
    
    execFile('python3', fullArgs, {
      timeout: options.timeout || 10000,
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    }, (error, stdout, stderr) => {
      if (error) {
        reject(new Error(`OKKI CLI 执行失败：${error.message}\n${stderr}`));
        return;
      }
      
      try {
        const result = JSON.parse(stdout);
        resolve(result);
      } catch (e) {
        resolve({ raw: stdout, stderr });
      }
    });
  });
}

/**
 * 加载已处理邮件记录
 */
function loadProcessedRecords() {
  try {
    if (fs.existsSync(CONFIG.processedFile)) {
      const data = fs.readFileSync(CONFIG.processedFile, 'utf8');
      return JSON.parse(data);
    }
  } catch (e) {
    console.error('加载已处理记录失败:', e.message);
  }
  return {};
}

/**
 * 保存已处理邮件记录
 */
function saveProcessedRecord(uid, metadata = {}) {
  try {
    const records = loadProcessedRecords();
    records[uid] = {
      processed_at: new Date().toISOString(),
      ...metadata
    };
    fs.writeFileSync(CONFIG.processedFile, JSON.stringify(records, null, 2));
    return true;
  } catch (e) {
    console.error('保存已处理记录失败:', e.message);
    return false;
  }
}

/**
 * 检查邮件是否已处理
 */
function isProcessed(uid) {
  const records = loadProcessedRecords();
  return !!records[uid];
}

/**
 * 记录未匹配邮件
 */
function logUnmatchedEmail(email, reason) {
  try {
    const timestamp = new Date().toISOString();
    const logLine = `${timestamp} | ${email} | ${reason}\n`;
    fs.appendFileSync(CONFIG.unmatchedLog, logLine);
  } catch (e) {
    console.error('写入未匹配日志失败:', e.message);
  }
}

// ==================== 核心功能 ====================

/**
 * 从邮箱地址提取域名
 */
function extractDomain(email) {
  if (!email || typeof email !== 'string') {
    return null;
  }
  const match = email.match(/@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$/);
  return match ? match[1].toLowerCase() : null;
}

/**
 * 检查域名是否为公共域名
 */
function isPublicDomain(domain) {
  if (!domain) return true;
  return CONFIG.publicDomains.includes(domain.toLowerCase());
}

/**
 * 通过域名搜索 OKKI 客户
 * 使用 OKKI CLI 的 company list 命令，通过 keyword 搜索
 */
async function searchByDomain(domain) {
  if (!domain || isPublicDomain(domain)) {
    return null;
  }
  
  try {
    // 使用 OKKI CLI 搜索客户（通过域名关键词）
    // execOkkiCli 自动添加 --json 标志
    const result = await execOkkiCli(['company', 'list', '-k', domain, '-l', '5']);
    
    if (result.data && result.data.length > 0) {
      // 精确匹配域名
      const exactMatch = result.data.find(company => {
        const companyDomain = extractDomain(company.website || company.email || '');
        return companyDomain === domain;
      });
      
      if (exactMatch) {
        return {
          company_id: exactMatch.company_id || exactMatch.id,
          name: exactMatch.name,
          match_type: 'domain_exact',
          confidence: 0.95
        };
      }
      
      // 部分匹配
      if (result.data.length > 0) {
        return {
          company_id: result.data[0].company_id || result.data[0].id,
          name: result.data[0].name,
          match_type: 'domain_partial',
          confidence: 0.7
        };
      }
    }
    
    return null;
  } catch (e) {
    console.error('域名搜索失败:', e.message);
    return null;
  }
}

/**
 * 通过向量搜索匹配客户
 */
async function searchByVector(email, subject = '', body = '') {
  try {
    // 构建搜索查询
    const query = `${email} ${subject || ''} ${body ? body.substring(0, 200) : ''}`.trim();
    
    if (!query) {
      return null;
    }
    
    const result = await execPython(CONFIG.customerSearchScript, [
      query,
      '--limit', '5',
      '--json'
    ]);
    
    if (result && Array.isArray(result) && result.length > 0) {
      const topMatch = result[0];
      return {
        company_id: topMatch.company_id,
        name: topMatch.name,
        match_type: 'vector',
        confidence: topMatch.score || 0.6,
        serial_id: topMatch.serial_id
      };
    }
    
    return null;
  } catch (e) {
    console.error('向量搜索失败:', e.message);
    return null;
  }
}

/**
 * 匹配客户
 * @param {string} email - 发件人或收件人邮箱
 * @param {string} subject - 邮件主题（可选，用于向量搜索）
 * @param {string} body - 邮件正文（可选，用于向量搜索）
 * @returns {Promise<{company_id: string, name: string, match_type: string, confidence: number} | null>}
 */
async function matchCustomer(email, subject = '', body = '') {
  if (!email) {
    return null;
  }
  
  const domain = extractDomain(email);
  
  // 步骤 1: 域名匹配（跳过公共域名）
  if (domain && !isPublicDomain(domain)) {
    const domainResult = await searchByDomain(domain);
    if (domainResult) {
      return domainResult;
    }
  }
  
  // 步骤 2: 向量搜索回退
  const vectorResult = await searchByVector(email, subject, body);
  if (vectorResult) {
    return vectorResult;
  }
  
  // 匹配失败
  logUnmatchedEmail(email, `domain=${domain}, vector_search=no_match`);
  return null;
}

/**
 * 创建邮件跟进记录
 * @param {string} companyId - OKKI 客户 ID
 * @param {object} emailData - 邮件数据
 * @param {string} emailData.uid - 邮件 UID（用于去重）
 * @param {string} emailData.from - 发件人
 * @param {string} emailData.to - 收件人
 * @param {string} emailData.subject - 主题
 * @param {string} emailData.date - 发送时间
 * @param {string} emailData.body - 正文摘要
 * @param {string} emailData.direction - in/out
 * @param {Array} emailData.attachments - 附件列表
 * @returns {Promise<object>}
 */
async function createEmailTrail(companyId, emailData) {
  // 去重检查
  if (emailData.uid && isProcessed(emailData.uid)) {
    return {
      success: false,
      reason: 'duplicate',
      message: '邮件已处理',
      uid: emailData.uid
    };
  }
  
  // 构建跟进内容
  const directionLabel = emailData.direction === 'in' ? '收到邮件' : '发送邮件';
  const attachmentList = emailData.attachments && emailData.attachments.length > 0
    ? `\n附件：${emailData.attachments.map(a => a.filename || a.name).join(', ')}`
    : '';
  
  const content = `${directionLabel}\n` +
    `主题：${emailData.subject}\n` +
    `时间：${emailData.date}\n` +
    `发件人：${emailData.from}\n` +
    `收件人：${emailData.to}\n` +
    `摘要：${emailData.body ? emailData.body.substring(0, 200) : '(无内容)'}${attachmentList}`;
  
  try {
    const result = await execOkkiCli([
      'trail', 'add',
      '--company', companyId,
      '--content', content,
      '--type', CONFIG.TRAIL_TYPE.EMAIL.toString()
    ]);
    
    if (result.error) {
      throw new Error(result.error);
    }
    
    // 记录已处理
    if (emailData.uid) {
      saveProcessedRecord(emailData.uid, {
        type: 'email',
        company_id: companyId,
        trail_id: result.trail_id || result.data?.trail_id
      });
    }
    
    return {
      success: true,
      company_id: companyId,
      trail_id: result.trail_id || result.data?.trail_id,
      action: 'trail.add'
    };
  } catch (e) {
    return {
      success: false,
      reason: 'api_error',
      message: e.message,
      company_id: companyId
    };
  }
}

/**
 * 创建报价单跟进记录
 * @param {string} companyId - OKKI 客户 ID
 * @param {object} quotationData - 报价单数据
 * @param {string} quotationData.uid - 报价单 UID（用于去重）
 * @param {string} quotationData.quotationNo - 报价单编号
 * @param {string} quotationData.date - 日期
 * @param {Array} quotationData.products - 产品列表
 * @param {number} quotationData.totalAmount - 总金额
 * @param {string} quotationData.validUntil - 有效期
 * @returns {Promise<object>}
 */
async function createQuotationTrail(companyId, quotationData) {
  // 去重检查
  if (quotationData.uid && isProcessed(quotationData.uid)) {
    return {
      success: false,
      reason: 'duplicate',
      message: '报价单已处理',
      uid: quotationData.uid
    };
  }
  
  // 构建产品列表字符串
  const productList = quotationData.products && quotationData.products.length > 0
    ? quotationData.products.map(p => `  - ${p.name || p.description} x ${p.quantity || 1}`).join('\n')
    : '(未列出产品)';
  
  const content = `报价单\n` +
    `编号：${quotationData.quotationNo}\n` +
    `日期：${quotationData.date}\n` +
    `总金额：${quotationData.totalAmount || '(未指定)'}\n` +
    `有效期：${quotationData.validUntil || '(未指定)'}\n` +
    `产品列表:\n${productList}`;
  
  try {
    const result = await execOkkiCli([
      'trail', 'add',
      '--company', companyId,
      '--content', content,
      '--type', CONFIG.TRAIL_TYPE.QUOTATION.toString()
    ]);
    
    if (result.error) {
      throw new Error(result.error);
    }
    
    // 记录已处理
    if (quotationData.uid) {
      saveProcessedRecord(quotationData.uid, {
        type: 'quotation',
        company_id: companyId,
        trail_id: result.trail_id || result.data?.trail_id,
        quotation_no: quotationData.quotationNo
      });
    }
    
    return {
      success: true,
      company_id: companyId,
      trail_id: result.trail_id || result.data?.trail_id,
      action: 'trail.add'
    };
  } catch (e) {
    return {
      success: false,
      reason: 'api_error',
      message: e.message,
      company_id: companyId
    };
  }
}

/**
 * 同步邮件到 OKKI（完整流程）
 * @param {object} emailData - 邮件数据
 * @returns {Promise<object>}
 */
async function syncEmailToOkki(emailData) {
  // 去重检查
  if (emailData.uid && isProcessed(emailData.uid)) {
    return {
      success: false,
      reason: 'duplicate',
      message: '邮件已处理',
      uid: emailData.uid
    };
  }
  
  // 匹配客户
  const customer = await matchCustomer(
    emailData.from || emailData.to,
    emailData.subject,
    emailData.body
  );
  
  if (!customer) {
    return {
      success: false,
      reason: 'customer_not_found',
      message: '未找到匹配的客户',
      email: emailData.from || emailData.to
    };
  }
  
  // 创建跟进记录
  const trailResult = await createEmailTrail(customer.company_id, {
    ...emailData,
    uid: emailData.uid
  });
  
  return {
    ...trailResult,
    customer
  };
}

// ==================== 测试模式 ====================

async function runTest() {
  console.log('🧪 OKKI Sync Module - 测试模式\n');
  
  // 测试 1: 域名提取
  console.log('测试 1: 域名提取');
  const testEmails = [
    'john@example.com',
    'sales@farreach-electronic.com',
    'invalid-email',
    'test@gmail.com'
  ];
  testEmails.forEach(email => {
    const domain = extractDomain(email);
    console.log(`  ${email} → ${domain} (公共域：${isPublicDomain(domain)})`);
  });
  
  // 测试 2: 去重机制
  console.log('\n测试 2: 去重机制');
  const testUid = `test-${Date.now()}`;
  console.log(`  创建测试记录：${testUid}`);
  saveProcessedRecord(testUid, { type: 'test' });
  console.log(`  检查是否已处理：${isProcessed(testUid)}`);
  
  // 测试 3: OKKI CLI 连接
  console.log('\n测试 3: OKKI CLI 连接');
  try {
    // execOkkiCli 自动添加 --json 标志
    const result = await execOkkiCli(['company', 'list', '-l', '1']);
    if (result.data) {
      console.log(`  ✓ OKKI CLI 正常，客户数量：${result.count || '未知'}`);
    } else {
      console.log(`  ✗ OKKI CLI 返回异常：${JSON.stringify(result)}`);
    }
  } catch (e) {
    console.log(`  ✗ OKKI CLI 连接失败：${e.message}`);
  }
  
  // 测试 4: 向量搜索连接
  console.log('\n测试 4: 向量搜索连接');
  try {
    const result = await execPython(CONFIG.customerSearchScript, ['test', '--limit', '1', '--json']);
    if (result) {
      console.log(`  ✓ 向量搜索正常`);
    } else {
      console.log(`  ✗ 向量搜索返回空`);
    }
  } catch (e) {
    console.log(`  ✗ 向量搜索失败：${e.message}`);
  }
  
  console.log('\n✅ 测试完成');
}

// ==================== 导出 ====================

module.exports = {
  // 核心功能
  matchCustomer,
  createEmailTrail,
  createQuotationTrail,
  syncEmailToOkki,
  
  // 工具函数
  extractDomain,
  isPublicDomain,
  isProcessed,
  loadProcessedRecords,
  saveProcessedRecord,
  
  // 配置
  CONFIG,
  
  // 测试
  runTest
};

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (command === 'test') {
    runTest().catch(console.error);
  } else if (command === 'quotation') {
    // 用法：node okki-sync.js quotation <json_string>
    // json_string 包含：{ "dataFile": "path/to/data.json", "quotationNo": "QT-xxx" }
    if (!args[1]) {
      console.log('用法：node okki-sync.js quotation <json_string>');
      console.log('json_string 示例：{"dataFile":"/path/to/data.json","quotationNo":"QT-20260314-001"}');
      process.exit(1);
    }
    
    (async () => {
      try {
        const params = JSON.parse(args[1]);
        const dataFile = params.dataFile;
        const quotationNo = params.quotationNo;
        
        if (!dataFile) {
          console.error('❌ 缺少 dataFile 参数');
          process.exit(1);
        }
        
        // 读取数据文件
        const data = JSON.parse(fs.readFileSync(dataFile, 'utf-8'));
        
        // 提取客户邮箱
        const customerEmail = data.customer?.email;
        const customerName = data.customer?.name || data.customer?.company_name || data.customer?.contact;
        
        if (!customerEmail && !customerName) {
          console.warn('⚠️  数据文件中缺少 customer.email 和 customer.name，无法匹配客户');
          // 记录未匹配
          fs.appendFileSync(CONFIG.unmatchedLog, `[${new Date().toISOString()}] quotation ${quotationNo || 'unknown'}: no customer email/name\n`);
          process.exit(0);
        }
        
        // 匹配客户
        console.log(`🔍 匹配客户：${customerEmail || customerName}...`);
        const customer = await matchCustomer(customerEmail || '', '', customerName || '');
        
        if (!customer) {
          console.warn(`⚠️  未找到匹配客户：${customerEmail || customerName}`);
          fs.appendFileSync(CONFIG.unmatchedLog, `[${new Date().toISOString()}] quotation ${quotationNo}: ${customerEmail || customerName} - no match\n`);
          process.exit(0);
        }
        
        console.log(`✓ 匹配成功：${customer.name} (${customer.company_id})`);
        
        // 构建报价单数据
        const products = data.products || [];
        const totalAmount = products.reduce((sum, p) => {
          // 支持多种字段格式：amount（预计算）、unit_price*quantity、unitPrice*quantity
          const lineTotal = p.amount || (p.quantity || 0) * (p.unit_price || p.unitPrice || 0);
          return sum + lineTotal;
        }, 0);
        
        // 支持两种数据格式：顶层字段（cable-germany.json）或嵌套 quotation 对象（farreach_5products.json）
        const quotationData = {
          uid: `quotation-${Date.now()}-${quotationNo || 'unknown'}`,
          quotationNo: quotationNo || data.quotationNo || data.quotation?.quotation_no || 'unknown',
          date: data.date || data.quotation?.date || new Date().toISOString().split('T')[0],
          products: products.map(p => ({
            name: p.description || p.name,
            quantity: p.quantity,
            unit_price: p.unit_price || p.unitPrice
          })),
          totalAmount: `${data.currency || 'USD'} ${totalAmount.toFixed(2)}`,
          validUntil: data.validUntil || data.quotation?.valid_until || data.quotation?.validUntil || '(未指定)'
        };
        
        // 创建跟进记录
        console.log(`📝 创建报价单跟进记录：${quotationData.quotationNo}...`);
        const result = await createQuotationTrail(customer.company_id, quotationData);
        
        if (result.success) {
          console.log(`✅ OKKI 跟进记录创建成功：${result.trail_id}`);
          process.exit(0);
        } else {
          console.error(`❌ OKKI 跟进记录创建失败：${result.reason} - ${result.message}`);
          process.exit(1);
        }
      } catch (e) {
        console.error(`❌ 执行失败：${e.message}`);
        process.exit(1);
      }
    })();
  } else {
    console.log('用法：node okki-sync.js test | quotation <json_string>');
    console.log('模块导出：matchCustomer, createEmailTrail, createQuotationTrail, syncEmailToOkki');
  }
}
