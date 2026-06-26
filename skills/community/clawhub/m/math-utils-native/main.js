const { execSync } = require('child_process');
const os = require('os');

/**
 * 核心逻辑：
 * 1. 识别操作系统
 * 2. 优先使用本地 CLI 工具 (bc, python3, awk)
 * 3. 构造并执行计算
 */

function calculate(expression) {
    const platform = os.platform(); // step 1: 检查操作系统
    let result = '';

    try {
        // step 2 & 3: 根据系统环境选择最优 CLI 计算器
        if (platform === 'linux' || platform === 'darwin') {
            // 优先检查 bc (高精度计算器)
            try {
                result = execSync(`echo "scale=10; ${expression}" | bc`, { encoding: 'utf-8' }).trim();
            } catch (e) {
                // 备选: python3
                result = execSync(`python3 -c "print(${expression})"`, { encoding: 'utf-8' }).trim();
            }
        } else if (platform === 'win32') {
            // Windows 环境使用 powershell
            result = execSync(`powershell "[Math]::Evaluate('${expression}')"`, { encoding: 'utf-8' }).trim();
        } else {
            throw new Error(`不支持的操作系统: ${platform}`);
        }

        // step 4: 返回核对后的结果
        return result;
    } catch (error) {
        return `计算出错: ${error.message}`;
    }
}

// 导出模块供 OpenClaw 调用
module.exports = { calculate };

// 简单命令行测试支持
if (require.main === module) {
    const expr = process.argv[2] || "1+1";
    console.log(`计算表达式: ${expr}`);
    console.log(`结果: ${calculate(expr)}`);
}
