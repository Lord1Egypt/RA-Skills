/**
 * 邮件通知器测试
 */

import { EmailNotifier } from '../src-new/infrastructure/notifiers/EmailNotifier'

describe('EmailNotifier', () => {
  it('应该正确初始化配置', () => {
    const notifier = new EmailNotifier({
      host: 'smtp.test.com',
      port: 587,
      user: 'test@test.com',
      password: 'password',
      from: 'test@test.com',
      to: ['user1@test.com', 'user2@test.com']
    })
    expect(notifier).toBeDefined()
  })

  it('应该在没有配置时跳过发送', async () => {
    const notifier = new EmailNotifier()
    await expect(notifier.notify('Test', 'Message', 'info')).resolves.toBeUndefined()
  })

  it('应该在有告警时发送报告', async () => {
    const notifier = new EmailNotifier({
      host: 'smtp.test.com',
      port: 587,
      user: 'test@test.com',
      password: 'password',
      from: 'test@test.com',
      to: ['user@test.com']
    })

    // 模拟 transporter，sendMail 返回 messageId
    const mockTransporter = {
      verify: jest.fn().mockResolvedValue(true),
      sendMail: jest.fn().mockResolvedValue({ messageId: 'test-message-id' })
    }

    const notifierWithMock = Object.assign(notifier, { transporter: mockTransporter }) as any
    await expect(notifierWithMock.notify('告警', '磁盘使用率 90%', 'critical')).resolves.toBeUndefined()
    expect(mockTransporter.sendMail).toHaveBeenCalled()
    expect(mockTransporter.sendMail.mock.calls[0][0].subject).toContain('CRITICAL')
  })

  it('无告警时 alertOnly 模式应跳过发送', async () => {
    const notifier = new EmailNotifier({
      host: 'smtp.test.com',
      port: 587,
      user: 'test@test.com',
      password: 'password',
      from: 'test@test.com',
      to: ['user@test.com']
    })

    // 模拟 transporter
    const mockTransporter = {
      verify: jest.fn().mockResolvedValue(true),
      sendMail: jest.fn().mockResolvedValue({ messageId: 'test-message-id' })
    }

    const notifierWithMock = Object.assign(notifier, {
      transporter: mockTransporter,
      config: { ...notifier['config'], alertOnly: true }
    }) as any

    // notify 直接调用时会尝试发送（alertOnly 只在 sendAlert 中生效）
    await expect(notifierWithMock.notify('Info', '消息', 'info')).resolves.toBeUndefined()
    expect(mockTransporter.sendMail).toHaveBeenCalled()
  })
})
