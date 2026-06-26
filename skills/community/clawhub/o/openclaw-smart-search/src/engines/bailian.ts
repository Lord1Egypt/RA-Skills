import { SecretManager } from '../key-manager';
import { SearchEngine, SearchResult, SearchOptions, QuotaInfo } from '../types';
import { validateSearchQuery } from '../utils/sanitize';
import { spawn, spawnSync } from 'child_process';

/**
 * 百炼搜索引擎适配器
 *
 * 安全说明：
 * 使用 spawn() 而非 exec() 执行外部命令，参数作为数组传递，不经过 shell 解析。
 * 这避免了 shell 注入攻击的风险。spawn() + shell: false 是安全的命令执行方式。
 */
export class BailianEngine implements SearchEngine {
  name = 'bailian';
  private secretManager = new SecretManager();

  async search(query: string, options: SearchOptions): Promise<SearchResult[]> {
    // 检查 mcporter 是否安装
    const mcporterCheck = spawnSync('which', ['mcporter'], { timeout: 5000 });
    if (mcporterCheck.status !== 0) {
      throw new Error(
        '⚠️  警告：mcporter 未安装\n' +
        '百炼搜索需要 mcporter 才能工作。\n\n' +
        '安装方法:\n' +
        '  npm install -g mcporter\n\n' +
        '配置方法:\n' +
        '  npm run setup:bailian\n\n' +
        '详见：https://github.com/openclaw/mcporter'
      );
    }

    // 验证和清理输入 - 防止注入攻击
    const safeQuery = validateSearchQuery(query);
    const safeCount = Math.min(parseInt((options.count || 5).toString()) || 5, 20);

    // 获取 API Key（带友好错误提示）
    let apiKey: string;
    try {
      apiKey = await this.secretManager.getEngineKey('bailian');
    } catch (error: any) {
      if (error.message.includes('not configured')) {
        throw new Error(
          '⚠️  百炼 API Key 未配置\n' +
          '请运行以下命令进行配置:\n' +
          '  npm run key:set bailian\n\n' +
          '获取 API Key: https://bailian.console.aliyun.com/'
        );
      }
      throw error;
    }

    // 使用 spawn 替代 exec，避免 shell 注入风险
    // 参数作为数组传递，不经过 shell 解析
    const result = await this.executeMcporter(apiKey, safeQuery, safeCount);

    return (result.pages || []).map((page: any) => ({
      title: page.title || '',
      url: page.url || '',
      snippet: page.snippet || '',
      engine: 'bailian',
      originalScore: 0.9
    }));
  }

  /**
   * 安全执行 mcporter 命令
   * 使用 spawn 避免命令注入，参数作为数组传递不经 shell 解析
   */
  private executeMcporter(
    apiKey: string,
    query: string,
    count: number
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      const timeout = 15000; // 15 秒超时
      let stdout = '';
      let stderr = '';

      // 使用 spawn，参数作为数组传递，避免 shell 注入
      const child = spawn(
        'mcporter',
        [
          'call',
          'WebSearch.bailian_web_search',
          `query=${query}`,
          `count=${count}`
        ],
        {
          env: { ...process.env, BAILIAN_MCP_API_KEY: apiKey },
          stdio: ['pipe', 'pipe', 'pipe'],
          shell: false, // 明确禁用 shell
          timeout: timeout
        }
      );

      // 设置整体超时
      const timer = setTimeout(() => {
        child.kill('SIGKILL');
        reject(new Error(
          `⏱️ 百炼搜索超时 (${timeout}ms)\n` +
          '可能原因:\n' +
          '  - 网络连接不稳定\n' +
          '  - API 服务繁忙\n\n' +
          '请稍后重试，或切换到其他引擎:\n' +
          '  npm run search "关键词" -- --engine=tavily'
        ));
      }, timeout);

      child.stdout?.on('data', (data: Buffer) => {
        stdout += data.toString('utf8');
      });

      child.stderr?.on('data', (data: Buffer) => {
        stderr += data.toString('utf8');
      });

      child.on('error', (err: Error) => {
        clearTimeout(timer);
        console.error('[Bailian] Process error:', err.message);

        if (err.message.includes('ENOENT')) {
          reject(new Error(
            '⚠️  mcporter 未找到\n' +
            '请安装: npm install -g mcporter'
          ));
        } else {
          reject(new Error(`百炼搜索进程错误: ${err.message}`));
        }
      });

      child.on('close', (code: number) => {
        clearTimeout(timer);

        if (stderr) {
          console.warn('[Bailian] Warning:', stderr.trim());
        }

        if (code !== 0) {
          console.error('[Bailian] Process exited with code:', code);
          reject(new Error(
            `百炼搜索失败 (退出码: ${code})\n` +
            '请检查:\n' +
            '  1. API Key 是否正确: npm run key:get bailian\n' +
            '  2. mcporter 配置是否正确: mcporter list'
          ));
          return;
        }

        try {
          const parsed = JSON.parse(stdout);
          resolve(parsed);
        } catch (parseErr: any) {
          console.error('[Bailian] JSON parse error:', parseErr.message);
          console.error('[Bailian] Raw output:', stdout.substring(0, 500));
          reject(new Error(
            `百炼响应解析错误\n` +
            '原始输出已记录到日志，请检查 mcporter 版本是否最新。'
          ));
        }
      });
    });
  }

  async checkQuota(): Promise<QuotaInfo> {
    // 百炼 MCP 免费版: 2000 次/月
    // 实际配额需登录控制台查询
    return { used: 0, limit: 2000, remaining: 2000 };
  }
}
