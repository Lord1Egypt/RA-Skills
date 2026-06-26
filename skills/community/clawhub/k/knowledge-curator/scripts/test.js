/**
 * test.js - 功能测试脚本
 * 
 * 测试 Knowledge Curator 的核心功能
 */

const path = require('path');
const fs = require('fs');

// 导入模块
const fetch = require('./fetch');
const summarize = require('./summarize');
const categorize = require('./categorize');
const store = require('./store');
const query = require('./query');
const main = require('./main');

// 测试配置
const TEST_CONFIG = {
  knowledgeBasePath: path.join(__dirname, '../knowledge-base'),
  indexPath: path.join(__dirname, '../knowledge-base/index.json'),
  categories: ['科技', '生活', '学习', '娱乐', '工作', '健康']
};

// 测试用例
const tests = [
  {
    name: '平台识别测试',
    test: () => {
      const urls = [
        'https://www.bilibili.com/video/BV1xx411c7mD',
        'https://www.zhihu.com/question/123456',
        'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'https://xiaohongshu.com/discovery/item/xxx',
        'https://example.com/page'
      ];
      
      const results = urls.map(url => ({
        url,
        platform: fetch.identifyPlatform(url)
      }));
      
      console.log('平台识别结果:');
      results.forEach(r => {
        console.log(`  ${r.url.substring(0, 50)}... → ${r.platform.name}`);
      });
      
      return results.every(r => r.platform.name !== null);
    }
  },
  
  {
    name: '内容分类测试',
    test: () => {
      const testCases = [
        {
          title: 'Python 编程入门教程',
          content: '学习 Python 编程语言，掌握基础语法和开发技能',
          expected: '学习'
        },
        {
          title: '最新 AI 技术突破',
          content: '人工智能领域取得重大进展，机器学习算法优化',
          expected: '科技'
        },
        {
          title: '职场沟通技巧',
          content: '提高工作效率，改善团队协作，管理技能提升',
          expected: '工作'
        },
        {
          title: '健康饮食指南',
          content: '营养搭配，运动健身，保持身体健康',
          expected: '健康'
        },
        {
          title: '电影推荐榜单',
          content: '最新影视作品，明星八卦，娱乐资讯',
          expected: '娱乐'
        }
      ];
      
      let passed = 0;
      testCases.forEach(tc => {
        const result = categorize.categorize(tc);
        const match = result.category === tc.expected;
        console.log(`  "${tc.title}" → ${result.category} ${match ? '✓' : '✗ (期望：' + tc.expected + ')'}`);
        if (match) passed++;
      });
      
      console.log(`分类准确率：${passed}/${testCases.length}`);
      return passed >= testCases.length * 0.8;
    }
  },
  
  {
    name: '内容总结测试',
    test: () => {
      const content = {
        title: '测试文章标题',
        content: '这是一段测试内容。包含多个句子。用于测试摘要生成功能。',
        description: '这是文章描述',
        tags: ['#测试', '#摘要'],
        keywords: ['测试', '摘要', '功能']
      };
      
      const result = summarize.processContent(content);
      
      console.log('总结结果:');
      console.log(`  标题：${result.title}`);
      console.log(`  摘要：${result.summary.substring(0, 50)}...`);
      console.log(`  知识点：${result.keyPoints.length}个`);
      console.log(`  标签：${result.tags.join(', ')}`);
      
      return result.summary.length > 0 && result.keyPoints.length > 0;
    }
  },
  
  {
    name: '存储功能测试',
    test: () => {
      const entry = {
        title: '测试条目 ' + Date.now(),
        url: 'https://example.com/test-' + Date.now(),
        content: '测试内容',
        category: '学习',
        tags: ['测试', '功能验证'],
        platform: '网页'
      };
      
      const result = store.storeEntry(entry, TEST_CONFIG);
      
      if (result.success) {
        console.log(`存储成功：${result.entry.id}`);
        console.log(`文件路径：${result.filePath}`);
        
        // 清理测试文件
        try {
          if (fs.existsSync(result.filePath)) {
            fs.unlinkSync(result.filePath);
          }
          // 从索引中移除
          const index = store.loadIndex(TEST_CONFIG.indexPath);
          index.entries = index.entries.filter(e => e.id !== result.entry.id);
          index.stats.total = index.entries.length;
          store.saveIndex(TEST_CONFIG.indexPath, index);
        } catch (e) {
          console.log('清理测试文件失败:', e.message);
        }
        
        return true;
      } else {
        console.log('存储失败:', result.reason);
        return false;
      }
    }
  },
  
  {
    name: '搜索功能测试',
    test: () => {
      // 先添加测试数据
      const testEntries = [
        { title: 'Python 教程', category: '学习', tags: ['Python', '编程'], url: 'https://test.com/1', content: 'Python 编程学习' },
        { title: 'JavaScript 入门', category: '学习', tags: ['JavaScript', '编程'], url: 'https://test.com/2', content: 'JS 入门教程' },
        { title: 'AI 技术解析', category: '科技', tags: ['AI', '技术'], url: 'https://test.com/3', content: '人工智能技术' }
      ];
      
      // 存储测试条目
      const stored = testEntries.map(e => store.storeEntry({
        ...e,
        platform: '测试'
      }, TEST_CONFIG));
      
      const storedIds = stored.filter(r => r.success).map(r => r.entry.id);
      
      // 执行搜索
      const results = query.search('编程', {}, TEST_CONFIG);
      console.log(`搜索"编程"找到 ${results.length} 条结果`);
      
      // 清理测试数据
      storedIds.forEach(id => {
        store.deleteEntry(id, TEST_CONFIG);
      });
      
      return results.length > 0;
    }
  },
  
  {
    name: '命令解析测试',
    test: () => {
      const commands = [
        { input: '/kb search Python', expected: { action: 'search', query: 'Python' } },
        { input: '/kb list 学习', expected: { action: 'list', category: '学习' } },
        { input: '/kb stats', expected: { action: 'stats' } },
        { input: '/kb view kb-123', expected: { action: 'view', entryId: 'kb-123' } }
      ];
      
      let passed = 0;
      commands.forEach(cmd => {
        const result = main.parseCommand(cmd.input);
        const match = result && result.action === cmd.expected.action;
        console.log(`  "${cmd.input}" → ${match ? '✓' : '✗'}`);
        if (match) passed++;
      });
      
      console.log(`命令解析准确率：${passed}/${commands.length}`);
      return passed === commands.length;
    }
  }
];

// 运行测试
async function runTests() {
  console.log('========================================');
  console.log('  Knowledge Curator 功能测试');
  console.log('========================================\n');
  
  let passed = 0;
  let failed = 0;
  
  for (const test of tests) {
    console.log(`\n🧪 测试：${test.name}`);
    console.log('----------------------------------------');
    
    try {
      const result = await test.test();
      if (result) {
        console.log(`✅ 通过`);
        passed++;
      } else {
        console.log(`❌ 失败`);
        failed++;
      }
    } catch (error) {
      console.log(`❌ 错误：${error.message}`);
      failed++;
    }
  }
  
  console.log('\n========================================');
  console.log(`  测试结果：${passed}通过 / ${failed}失败`);
  console.log('========================================\n');
  
  return failed === 0;
}

// 执行测试
if (require.main === module) {
  runTests()
    .then(success => {
      process.exit(success ? 0 : 1);
    })
    .catch(err => {
      console.error('测试执行失败:', err.message);
      process.exit(1);
    });
}

module.exports = { runTests, tests };
