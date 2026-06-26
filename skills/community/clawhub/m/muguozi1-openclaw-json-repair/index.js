#!/usr/bin/env node
/**
 * JSON 自动修复工具
 * 
 * 灵感来源：karpathy/llm.c - 简单、可读、教育优先
 * 
 * 功能:
 * - 修复尾随逗号
 * - 修复未引号键
 * - 移除注释
 * - 修复单引号
 * 
 * 用法:
 *   node index.js --text="{a:1,}"
 *   node index.js --file=config.json
 *   node index.js --test
 */

const fs = require('fs');
const path = require('path');

/**
 * 修复 JSON 字符串
 * 
 * @param {string} jsonString - 需要修复的 JSON 字符串
 * @param {object} options - 选项
 * @param {boolean} options.verbose - 详细模式
 * @returns {object} 修复后的 JSON 对象
 * 
 * 示例:
 *   repairJSON('{a:1,}') // 返回 {a: 1}
 *   repairJSON('{a:1,}', { verbose: true })
 */
function repairJSON(jsonString, options = {}) {
    const { verbose = false } = options;
    let fixed = jsonString;
    const fixes = [];
    
    if (verbose) console.log('开始修复 JSON...\n');
    
    // 1. 移除单行注释 (// ...)
    const beforeComments = fixed;
    fixed = fixed.replace(/\/\/.*$/gm, '');
    if (fixed !== beforeComments) {
        fixes.push('移除单行注释');
    }
    
    // 2. 移除多行注释 (/* ... */)
    const beforeMultiComments = fixed;
    fixed = fixed.replace(/\/\*[\s\S]*?\*\//g, '');
    if (fixed !== beforeMultiComments) {
        fixes.push('移除多行注释');
    }
    
    // 3. 替换单引号为双引号
    const beforeQuotes = fixed;
    // 简单处理：替换键和字符串值的单引号
    fixed = fixed.replace(/'/g, '"');
    if (fixed !== beforeQuotes) {
        fixes.push('替换单引号为双引号');
    }
    
    // 4. 修复未引号的键
    const beforeKeys = fixed;
    fixed = fixed.replace(/([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:/g, '$1"$2":');
    if (fixed !== beforeKeys) {
        fixes.push('修复未引号的键');
    }
    
    // 5. 移除尾随逗号
    const beforeTrailing = fixed;
    fixed = fixed.replace(/,(\s*[}\]])/g, '$1');
    if (fixed !== beforeTrailing) {
        fixes.push('移除尾随逗号');
    }
    
    // 6. 尝试解析
    try {
        const result = JSON.parse(fixed);
        if (verbose) {
            console.log('✅ 修复成功!');
            console.log('应用的修复:', fixes);
        }
        return result;
    } catch (e) {
        if (verbose) {
            console.log('❌ 修复失败:', e.message);
            console.log('修复后的内容:', fixed);
        }
        throw new Error(`JSON 修复失败：${e.message}`);
    }
}

/**
 * 从文本中提取并修复 JSON
 * 
 * @param {string} text - 包含 JSON 的文本
 * @returns {object} 解析后的 JSON 对象
 * 
 * 示例:
 *   const llmOutput = `Here's the JSON: {a:1}`;
 *   extractAndRepairJSON(llmOutput);
 */
function extractAndRepairJSON(text) {
    // 尝试找到第一个 { 和最后一个 }
    const start = text.indexOf('{');
    const end = text.lastIndexOf('}');
    
    if (start === -1 || end === -1) {
        throw new Error('未找到 JSON 对象');
    }
    
    const jsonString = text.substring(start, end + 1);
    return repairJSON(jsonString);
}

/**
 * 运行测试
 */
function runTests() {
    console.log('\n🧪 Running tests...\n');
    
    const tests = [
        {
            name: 'Test 1: Trailing comma + unquoted key',
            input: '{a:1,}',
            expected: { a: 1 }
        },
        {
            name: 'Test 2: Trailing comma in array',
            input: '[1,2,3,]',
            expected: [1, 2, 3]
        },
        {
            name: 'Test 3: Comment',
            input: '{// comment\n"a":1}',
            expected: { a: 1 }
        },
        {
            name: 'Test 4: Single quotes',
            input: "{'a':'b'}",
            expected: { a: 'b' }
        },
        {
            name: 'Test 5: Multiple issues',
            input: "{// comment\nname: 'test',}",
            expected: { name: 'test' }
        }
    ];
    
    let passed = 0;
    let failed = 0;
    
    tests.forEach((test, i) => {
        try {
            const result = repairJSON(test.input);
            const match = JSON.stringify(result) === JSON.stringify(test.expected);
            
            if (match) {
                console.log(`✓ ${test.name} PASSED`);
                passed++;
            } else {
                console.log(`✗ ${test.name} FAILED`);
                console.log(`  Expected: ${JSON.stringify(test.expected)}`);
                console.log(`  Got: ${JSON.stringify(result)}`);
                failed++;
            }
        } catch (e) {
            console.log(`✗ ${test.name} FAILED: ${e.message}`);
            failed++;
        }
    });
    
    console.log(`\n📊 Results: ${passed}/${tests.length} passed\n`);
    
    if (failed > 0) {
        process.exit(1);
    } else {
        console.log('✅ All tests passed!\n');
        process.exit(0);
    }
}

/**
 * 主函数 - CLI 入口
 */
function main() {
    const args = process.argv.slice(2);
    
    // 解析参数
    const argMap = {};
    for (let i = 0; i < args.length; i++) {
        if (args[i].startsWith('--')) {
            const [key, value] = args[i].substring(2).split('=');
            argMap[key] = value || true;
        }
    }
    
    // 运行测试
    if (argMap.test) {
        runTests();
        return;
    }
    
    // 修复文本
    if (argMap.text) {
        try {
            const result = repairJSON(argMap.text, { verbose: true });
            console.log('\n修复结果:');
            console.log(JSON.stringify(result, null, 2));
        } catch (e) {
            console.error('错误:', e.message);
            process.exit(1);
        }
        return;
    }
    
    // 修复文件
    if (argMap.file) {
        const filePath = argMap.file === true ? args[args.length - 1] : argMap.file;
        
        if (!fs.existsSync(filePath)) {
            console.error(`错误：文件不存在：${filePath}`);
            process.exit(1);
        }
        
        try {
            const content = fs.readFileSync(filePath, 'utf-8');
            const result = repairJSON(content, { verbose: true });
            
            // 创建备份
            if (argMap.backup) {
                const backupPath = filePath + '.bak';
                fs.copyFileSync(filePath, backupPath);
                console.log(`已创建备份：${backupPath}`);
            }
            
            // 写回文件
            fs.writeFileSync(filePath, JSON.stringify(result, null, 2));
            console.log(`\n✅ 文件已修复：${filePath}`);
        } catch (e) {
            console.error('错误:', e.message);
            process.exit(1);
        }
        return;
    }
    
    // 显示帮助
    console.log(`
JSON 自动修复工具

用法:
  node index.js --text="{a:1,}"     # 修复 JSON 字符串
  node index.js --file=config.json  # 修复 JSON 文件
  node index.js --test              # 运行测试
  node index.js --help              # 显示帮助

选项:
  --text      JSON 字符串
  --file      JSON 文件路径
  --backup    修复文件时创建备份
  --test      运行测试
  --verbose   详细模式
  --help      显示帮助

示例:
  node index.js --text="{a:1,}" --verbose
  node index.js --file=config.json --backup
`);
}

// 导出函数
module.exports = {
    repairJSON,
    extractAndRepairJSON,
    runTests
};

// 运行主函数
if (require.main === module) {
    main();
}
