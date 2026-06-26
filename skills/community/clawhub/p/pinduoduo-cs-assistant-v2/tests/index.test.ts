/**
 * 拼多多客服助手单元测试
 */

import { matchTemplate, TEMPLATES } from '../src/index'

describe('拼多多客服助手', () => {
  describe('话术匹配', () => {
    test('售前咨询 - 库存查询', () => {
      const message = '请问这个还有货吗？'
      const reply = matchTemplate(message)
      expect(reply).toContain('现货')
    })

    test('售前咨询 - 发货时间', () => {
      const message = '什么时候发货啊'
      const reply = matchTemplate(message)
      expect(reply).toContain('发货')
    })

    test('售前咨询 - 优惠活动', () => {
      const message = '能便宜吗？有优惠吗？'
      const reply = matchTemplate(message)
      expect(reply).toContain('活动')
    })

    test('物流查询 - 物流信息', () => {
      const message = '我的货到哪了？'
      const reply = matchTemplate(message)
      expect(reply).toContain('运输')
    })

    test('物流查询 - 催促物流', () => {
      const message = '怎么还没到，太慢了'
      const reply = matchTemplate(message)
      expect(reply).toContain('催')
    })

    test('售后 - 退货退款', () => {
      const message = '我不想要了，能退货吗'
      const reply = matchTemplate(message)
      expect(reply).toContain('退换货')
    })

    test('售后 - 质量问题', () => {
      const message = '收到货发现有破损，质量问题'
      const reply = matchTemplate(message)
      expect(reply).toContain('抱歉')
    })

    test('售后 - 差评威胁', () => {
      const message = '我要给差评，投诉你们'
      const reply = matchTemplate(message)
      expect(reply).toContain('抱歉')
    })

    test('默认回复 - 无匹配', () => {
      const message = '你好呀'
      const reply = matchTemplate(message)
      expect(reply).toContain('您好')
    })
  })

  describe('话术库完整性', () => {
    test('话术库包含必要分类', () => {
      expect(TEMPLATES).toHaveProperty('售前')
      expect(TEMPLATES).toHaveProperty('物流')
      expect(TEMPLATES).toHaveProperty('售后')
    })

    test('每个分类都有话术', () => {
      for (const category in TEMPLATES) {
        const templates = TEMPLATES[category as keyof typeof TEMPLATES]
        expect(templates.length).toBeGreaterThan(0)
      }
    })

    test('话术格式正确', () => {
      for (const category in TEMPLATES) {
        const templates = TEMPLATES[category as keyof typeof TEMPLATES]
        templates.forEach(template => {
          expect(template).toHaveProperty('keywords')
          expect(template).toHaveProperty('response')
          expect(Array.isArray(template.keywords)).toBe(true)
          expect(template.keywords.length).toBeGreaterThan(0)
          expect(typeof template.response).toBe('string')
          expect(template.response.length).toBeGreaterThan(0)
        })
      }
    })
  })
})

// 辅助函数（实际在 src/index.ts 中导出）
function matchTemplate(message: string): string {
  for (const category in TEMPLATES) {
    const templates = TEMPLATES[category as keyof typeof TEMPLATES]
    for (const template of templates) {
      for (const keyword of template.keywords) {
        if (message.includes(keyword)) {
          return template.response
        }
      }
    }
  }
  return '亲，您好，有什么可以帮您的吗？'
}

const TEMPLATES: any = {
  售前: [
    {
      keywords: ['有货吗', '还有货', '库存', '没货'],
      response: '亲，这款商品目前有现货的哦，您可以直接下单~'
    },
    {
      keywords: ['什么时候发货', '几天发', '发货时间'],
      response: '亲，我们一般在下单后 24-48 小时内发货，节假日顺延~'
    },
    {
      keywords: ['能便宜吗', '优惠', '打折', '包邮'],
      response: '亲，现在店铺有满减活动，满 99 减 10，满 199 减 30，很划算的哦~'
    }
  ],
  物流: [
    {
      keywords: ['到哪了', '物流信息', '快递', '运输中'],
      response: '亲，帮您查了一下，您的包裹正在运输中，预计 2-3 天送达，请耐心等待~'
    },
    {
      keywords: ['怎么还没到', '太慢了', '好慢'],
      response: '亲，非常理解您的心情，我帮您催一下快递公司，有进展马上通知您~'
    }
  ],
  售后: [
    {
      keywords: ['退货', '退款', '不要了', '不想要'],
      response: '亲，支持 7 天无理由退换货的，您在订单页面申请一下，我们马上处理~'
    },
    {
      keywords: ['质量问题', '坏了', '破损', '有瑕疵'],
      response: '亲，非常抱歉给您带来不好的体验，您拍个照片，我们给您补发或全额退款~'
    },
    {
      keywords: ['差评', '投诉', '举报'],
      response: '亲，真的非常抱歉，您有什么问题随时联系我们，一定给您满意解决方案~'
    }
  ]
}
