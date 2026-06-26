/**
 * Browser Controller - UI Automation SOP
 * 
 * 这个脚本定义了在没有 API 的情况下，如何通过浏览器访问 OTA 后台进行操作。
 * 它可以被支持浏览器工具的 Agent (如 Antigravity 或 openclaw) 直接解析执行。
 */

const PLATFORM_URLS = {
  ctrip: 'https://ebooking.ctrip.com/',
  meituan: 'https://eb.meituan.com/hotel/',
  fliggy: 'https://b.fliggy.com/'
};

class BrowserController {
  /**
   * 引导 Agent 执行改价流程的描述 (Prompt-based Instructions)
   */
  async getPriceUpdateSOP(platform, roomType, date, newPrice) {
    return {
      target_url: PLATFORM_URLS[platform],
      steps: [
        `1. 导航到 ${PLATFORM_URLS[platform]} 并确保已登录。`,
        `2. 在侧边栏寻找“价格维护”或“房态房价”菜单并点击。`,
        `3. 在日期筛选器中选择 ${date}。`,
        `4. 定位到房型名称为 "${roomType}" 的行。`,
        `5. 找到对应的价格输入框，将其值修改为 "${newPrice}"。`,
        `6. 点击页面底部的“保存”或“提交”按钮。`,
        `7. 截图并确认页面显示“修改成功”字样。`
      ],
      selectors: {
        // 预设一些常见的选择器（示例，需根据实际 DOM 调整）
        price_input: `input[data-room="${roomType}"][data-date="${date}"]`,
        save_button: 'button#btn-save-all'
      }
    };
  }
}

module.exports = new BrowserController();
