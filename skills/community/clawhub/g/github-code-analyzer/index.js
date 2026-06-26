const axios = require('axios');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const ARK_API_KEY = "3ee94c45-6dad-4680-827c-eb3017420dff";

const MODELS = {
  deepseek: 'deepseek-v3-2-251201',
  'deepseek-coder': 'deepseek-v3-2-251201',  // 用同一个模型，代码分析更强
  minimax: 'MiniMax-M2.5'
};

module.exports = {
  name: 'github-code-analyzer',
  description: '分析 GitHub 项目代码质量。支持模型：deepseek, deepseek-coder',
  
  async execute(params) {
    const repoUrl = params.repo || params.url || params[0];
    const modelName = params.model || params.model || 'deepseek';
    
    if (!repoUrl) {
      return { text: '请提供 GitHub 仓库地址，例如：\n分析 https://github.com/xxx/xxx\n\n可用模型：deepseek, deepseek-coder\n用法：分析 xxx --model deepseek-coder', success: false };
    }

    // 提取 owner/repo
    const match = repoUrl.match(/github\.com\/([^\/]+)\/([^\/]+)/);
    if (!match) {
      return { text: '无效的 GitHub 地址', success: false };
    }

    const [, owner, repo] = match;
    const tempDir = path.join(os.tmpdir(), `gh-analysis-${Date.now()}`);

    try {
      // 1. 克隆仓库
      await execAsync(`git clone --depth 1 ${repoUrl} ${tempDir}`, 60000);
      
      // 2. 列出项目结构
      const structure = await getProjectStructure(tempDir);
      
      // 3. 读取代码文件
      const codeSamples = await getCodeSamples(tempDir);
      
      // 4. DeepSeek 分析
      const analysis = await analyzeWithDeepSeek(owner, repo, structure, codeSamples, modelName);
      
      // 清理
      fs.rmSync(tempDir, { recursive: true, force: true });
      
      return { text: analysis, success: true };
      
    } catch (error) {
      // 清理
      if (fs.existsSync(tempDir)) {
        fs.rmSync(tempDir, { recursive: true, force: true });
      }
      return { text: `分析失败：${error.message}`, success: false };
    }
  }
};

function execAsync(cmd, timeout) {
  return new Promise((resolve, reject) => {
    exec(cmd, { timeout }, (err, stdout, stderr) => {
      if (err) reject(err);
      else resolve(stdout);
    });
  });
}

async function getProjectStructure(dir, maxDepth = 3) {
  const result = [];
  function walk(dir, depth = 0) {
    if (depth > maxDepth) return;
    const items = fs.readdirSync(dir);
    for (const item of items.slice(0,15)) {
      if (item.startsWith('.')) continue;
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      result.push('  '.repeat(depth) + (stat.isDirectory() ? '📁 ' + item : '📄 ' + item));
      if (stat.isDirectory()) walk(fullPath, depth + 1);
    }
  }
  walk(dir);
  return result.slice(0, 50).join('\n');
}

async function getCodeSamples(dir) {
  const extensions = ['.js', '.ts', '.py', '.go', '.java', '.cpp'];
  const samples = [];
  
  function findFiles(dir) {
    const items = fs.readdirSync(dir);
    for (const item of items) {
      if (samples.length >= 3) return;
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      if (stat.isDirectory() && !item.startsWith('.') && item !== 'node_modules') {
        findFiles(fullPath);
      } else if (extensions.some(ext => item.endsWith(ext))) {
        const content = fs.readFileSync(fullPath, 'utf-8').slice(0, 2000);
        samples.push(`📄 ${item}\n\`\`\`\n${content}\n\`\`\``);
      }
    }
  }
  
  findFiles(dir);
  return samples.join('\n\n');
}

async function analyzeWithDeepSeek(owner, repo, structure, codeSamples, modelName = 'deepseek') {
  const model = MODELS[modelName] || MODELS.deepseek;
  
  const prompt = `请分析 GitHub 项目 ${owner}/${repo}：

## 项目结构
${structure}

## 代码示例
${codeSamples}

请从以下角度分析（用中文）：
1. 代码质量（架构、可读性、规范）
2. 潜在 bug 或安全隐患
3. 改进建议
4. 技术栈评估

只输出分析结果，不需要打招呼。`;

  try {
    const response = await axios.post(
      'https://ark.cn-beijing.volces.com/api/v3/chat/completions',
      {
        model: model,
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.7
      },
      { timeout: 60000 }
    );

    return `🔍 ${owner}/${repo} 代码分析 (${modelName})\n\n` + response.data.choices[0].message.content;
  } catch (e) {
    return `⚠️ ${modelName} 分析失败，但项目结构已获取：\n\n${structure}`;
  }
}
