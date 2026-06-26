/**
 * Git Commit Helper - 智能 Git Commit Message 生成器
 * 根据代码变更自动生成规范的 commit message
 */

const { execSync } = require('child_process');

// 提交类型定义
const COMMIT_TYPES = {
  feat: { label: '新功能', priority: 1 },
  fix: { label: '修复', priority: 2 },
  docs: { label: '文档', priority: 3 },
  style: { label: '格式', priority: 4 },
  refactor: { label: '重构', priority: 5 },
  test: { label: '测试', priority: 6 },
  chore: { label: '杂项', priority: 7 }
};

// 文件扩展名到类型的映射
const FILE_TYPE_MAP = {
  '.md': 'docs',
  '.txt': 'docs',
  '.css': 'style',
  '.scss': 'style',
  '.less': 'style',
  '.test.js': 'test',
  '.spec.js': 'test',
  '.test.ts': 'test',
  '.spec.ts': 'test',
  '.json': 'chore',
  '.yml': 'chore',
  '.yaml': 'chore',
  '.env': 'chore'
};

// 主函数：生成 commit message
async function generateCommitMessage(options = {}) {
  const result = {
    success: false,
    message: '',
    changes: null,
    error: null
  };

  try {
    // 1. 获取 git diff
    const diff = getGitDiff();
    
    if (!diff || diff.trim() === '') {
      result.error = '没有检测到代码变更，请先 git add 添加文件';
      return result;
    }

    // 2. 分析变更
    const analysis = analyzeChanges(diff);
    result.changes = analysis;

    // 3. 生成 commit message
    result.message = buildCommitMessage(analysis, options);
    result.success = true;

    return result;
  } catch (error) {
    result.error = error.message;
    return result;
  }
}

// 获取 git diff
function getGitDiff() {
  try {
    // 检查是否在 git 仓库中
    execSync('git rev-parse --git-dir', { stdio: 'pipe' });
    
    // 获取暂存区的 diff
    const diff = execSync('git diff --cached --stat', { 
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    return diff;
  } catch (error) {
    if (error.status === 128) {
      throw new Error('当前目录不是 git 仓库');
    }
    throw error;
  }
}

// 分析代码变更
function analyzeChanges(diff) {
  const analysis = {
    files: [],
    types: {},
    scope: '',
    summary: [],
    type: 'feat'
  };

  const lines = diff.trim().split('\n');
  
  lines.forEach(line => {
    const match = line.match(/(.+?)\s+\|\s+(\d+)\s+([+\-]+)/);
    if (match) {
      const filePath = match[1].trim();
      const changes = parseInt(match[2]);
      const indicators = match[3];
      
      const additions = (indicators.match(/\+/g) || []).length;
      const deletions = (indicators.match(/-/g) || []).length;

      analysis.files.push({
        path: filePath,
        changes,
        additions,
        deletions
      });

      // 推断类型
      const ext = '.' + filePath.split('.').pop();
      const inferredType = FILE_TYPE_MAP[ext] || 'feat';
      analysis.types[inferredType] = (analysis.types[inferredType] || 0) + 1;

      // 提取 scope（目录名或模块名）
      const parts = filePath.split('/');
      if (parts.length > 1) {
        const scope = parts[0];
        analysis.scope = scope;
      }
    }
  });

  // 确定主要类型
  const sortedTypes = Object.entries(analysis.types)
    .sort((a, b) => b[1] - a[1]);
  
  if (sortedTypes.length > 0) {
    analysis.type = sortedTypes[0][0];
  }

  // 生成变更摘要
  analysis.summary = generateSummary(analysis);

  return analysis;
}

// 生成变更摘要
function generateSummary(analysis) {
  const summaries = [];
  
  analysis.files.forEach(file => {
    const fileName = file.path.split('/').pop();
    
    if (file.additions > 0 && file.deletions === 0) {
      summaries.push(`新增 ${fileName}`);
    } else if (file.deletions > 0 && file.additions === 0) {
      summaries.push(`删除 ${fileName}`);
    } else {
      summaries.push(`更新 ${fileName}`);
    }
  });

  return summaries;
}

// 构建 commit message
function buildCommitMessage(analysis, options = {}) {
  const { language = 'zh' } = options;
  
  const typeInfo = COMMIT_TYPES[analysis.type] || COMMIT_TYPES.feat;
  const scope = analysis.scope ? `(${analysis.scope})` : '';
  
  // 生成标题
  let title = '';
  if (language === 'zh') {
    title = `${analysis.type}${scope}: ${generateChineseTitle(analysis)}`;
  } else {
    title = `${analysis.type}${scope}: ${generateEnglishTitle(analysis)}`;
  }

  // 生成正文
  const body = analysis.summary.map(s => `- ${s}`).join('\n');

  // 完整 message
  let message = title;
  if (body) {
    message += `\n\n${body}`;
  }

  return message;
}

// 生成中文标题
function generateChineseTitle(analysis) {
  const typeLabels = {
    feat: '添加新功能',
    fix: '修复问题',
    docs: '更新文档',
    style: '调整格式',
    refactor: '代码重构',
    test: '添加测试',
    chore: '更新配置'
  };

  const baseTitle = typeLabels[analysis.type] || '更新代码';
  
  if (analysis.files.length === 1) {
    const fileName = analysis.files[0].path.split('/').pop();
    return `${baseTitle} - ${fileName}`;
  }

  return `${baseTitle} (${analysis.files.length} 个文件)`;
}

// 生成英文标题
function generateEnglishTitle(analysis) {
  const typeLabels = {
    feat: 'Add new feature',
    fix: 'Fix issue',
    docs: 'Update documentation',
    style: 'Update code style',
    refactor: 'Refactor code',
    test: 'Add tests',
    chore: 'Update configuration'
  };

  const baseTitle = typeLabels[analysis.type] || 'Update code';
  
  if (analysis.files.length === 1) {
    const fileName = analysis.files[0].path.split('/').pop();
    return `${baseTitle} - ${fileName}`;
  }

  return `${baseTitle} (${analysis.files.length} files)`;
}

// 导出技能接口
module.exports = {
  name: 'git-commit-helper',
  version: '1.0.0',
  description: '智能 Git Commit Message 生成器',
  
  // 技能执行入口
  async execute(params) {
    const { language = 'zh' } = params || {};
    return await generateCommitMessage({ language });
  },

  // 技能元数据
  meta: {
    author: '倒里牢数',
    license: 'MIT',
    tags: ['git', 'commit', 'developer', 'automation'],
    category: 'developer-tools'
  }
};
