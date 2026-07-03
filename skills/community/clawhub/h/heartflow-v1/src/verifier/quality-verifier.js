/**
 * 质量验证器 (Quality Verifier) v1.0.0
 *
 * 验证执行结果的质量，不只是检查 success
 */

class QualityVerifier {
  constructor() {
    this.rules = new Map();
    this._registerDefaultRules();
  }

  /**
   * 注册验证规则
   */
  registerRule(name, rule) {
    this.rules.set(name, {
      name,
      check: rule.check,
      weight: rule.weight || 1,
      critical: rule.critical || false
    });
  }

  /**
   * 验证质量
   */
  verify(result, context = {}) {
    const results = [];
    let totalWeight = 0;
    let passedWeight = 0;
    let criticalFailed = false;

    for (const [name, rule] of this.rules) {
      try {
        const checkResult = rule.check(result, context);
        results.push({
          rule: name,
          passed: checkResult.passed,
          weight: rule.weight,
          critical: rule.critical,
          message: checkResult.message || '',
          details: checkResult.details || null
        });

        totalWeight += rule.weight;
        if (checkResult.passed) {
          passedWeight += rule.weight;
        }

        if (rule.critical && !checkResult.passed) {
          criticalFailed = true;
        }
      } catch (error) {
        results.push({
          rule: name,
          passed: false,
          weight: rule.weight,
          critical: rule.critical,
          error: error.message
        });
      }
    }

    const qualityScore = totalWeight > 0 ? (passedWeight / totalWeight) : 0;

    return {
      passed: !criticalFailed && qualityScore >= 0.7,
      qualityScore,
      qualityLevel: this._getQualityLevel(qualityScore),
      results,
      criticalFailed,
      summary: {
        total: results.length,
        passed: results.filter(r => r.passed).length,
        failed: results.filter(r => !r.passed).length
      }
    };
  }

  /**
   * 获取质量等级
   */
  _getQualityLevel(score) {
    if (score >= 0.95) return 'excellent';
    if (score >= 0.85) return 'good';
    if (score >= 0.7) return 'acceptable';
    if (score >= 0.5) return 'poor';
    return 'critical';
  }

  /**
   * 注册默认规则
   */
  _registerDefaultRules() {
    // 1. 成功状态
    this.registerRule('success_check', {
      check: (result) => ({
        passed: result.success !== false,
        message: result.success ? '执行成功' : '执行失败'
      }),
      weight: 2,
      critical: true
    });

    // 2. 非空输出
    this.registerRule('has_output', {
      check: (result) => {
        const output = result.stdout || result.stderr || result.output || result.body || '';
        const hasContent = output.trim().length > 0;
        return {
          passed: hasContent,
          message: hasContent ? '有输出内容' : '无输出'
        };
      },
      weight: 1
    });

    // 3. 无错误模式
    this.registerRule('no_error_patterns', {
      check: (result) => {
        const output = result.stdout || result.stderr || '';
        const errorPatterns = [
          /error[:\s]/i,
          /fail(ed)?/i,
          /exception/i,
          /traceback/i,
          /cannot\s+find/i,
          /command\s+not\s+found/i
        ];

        const foundErrors = errorPatterns.filter(p => p.test(output));
        return {
          passed: foundErrors.length === 0,
          message: foundErrors.length === 0 ? '无错误模式' : `发现 ${foundErrors.length} 个错误模式`
        };
      },
      weight: 1,
      critical: true
    });

    // 4. 预期内容存在
    this.registerRule('expected_content', {
      check: (result, context) => {
        if (!context.expectedContent) return { passed: true, message: '未指定预期内容' };

        const output = result.stdout || result.stderr || result.output || '';
        const hasContent = output.includes(context.expectedContent);
        return {
          passed: hasContent,
          message: hasContent ? '包含预期内容' : '不包含预期内容'
        };
      },
      weight: 2
    });

    // 5. 退出码
    this.registerRule('exit_code', {
      check: (result, context) => {
        const expectedCode = context.expectedExitCode || 0;
        const actualCode = result.exitCode;

        if (actualCode === undefined || actualCode === null) {
          return { passed: true, message: '无退出码' };
        }

        return {
          passed: actualCode === expectedCode,
          message: actualCode === expectedCode ? `退出码正确: ${actualCode}` : `退出码错误: ${actualCode}`
        };
      },
      weight: 1.5,
      critical: true
    });

    // 6. 输出长度合理
    this.registerRule('output_length', {
      check: (result, context) => {
        const output = result.stdout || result.stderr || '';
        const minLength = context.minOutputLength || 0;
        const maxLength = context.maxOutputLength || 100000;

        const length = output.trim().length;
        const isValid = length >= minLength && length <= maxLength;

        return {
          passed: isValid,
          message: isValid ? `输出长度合理: ${length}` : `输出长度异常: ${length}`
        };
      },
      weight: 0.5
    });
  }

  /**
   * 快速验证
   */
  quickVerify(result) {
    return {
      success: result.success !== false,
      hasOutput: !!(result.stdout || result.stderr || result.output),
      qualityScore: this.verify(result).qualityScore
    };
  }
}

module.exports = { QualityVerifier };
