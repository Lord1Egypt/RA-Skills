/**
 * i18n 单元测试
 */

import { t, getSystemLanguage, type Language } from '../skills/ops-maintenance/src/utils/i18n'

describe('i18n', () => {
  it('应该返回中文翻译', () => {
    expect(t('unknown_action', 'zh')).toBe('未知操作')
    expect(t('health_check', 'zh')).toBe('系统健康检查')
    expect(t('log_analysis', 'zh')).toBe('日志分析')
  })

  it('应该返回英文翻译', () => {
    expect(t('unknown_action', 'en')).toBe('Unknown action')
    expect(t('health_check', 'en')).toBe('System Health Check')
    expect(t('log_analysis', 'en')).toBe('Log Analysis')
  })

  it('不存在的key应该返回原key', () => {
    expect(t('nonexistent_key', 'zh')).toBe('nonexistent_key')
    expect(t('nonexistent_key', 'en')).toBe('nonexistent_key')
  })

  it('不存在的语言应该返回原key', () => {
    expect(t('unknown_action', 'ja' as Language)).toBe('unknown_action')
  })
})
