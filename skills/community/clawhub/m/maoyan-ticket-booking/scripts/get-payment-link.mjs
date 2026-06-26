/**
 * get-payment-link.mjs — 生成猫眼订单支付链接
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   无需参数（返回带渠道参数的支付链接）
 *
 * 本地调试示例：
 *   node scripts/get-payment-link.mjs
 *   echo '{}' | node scripts/get-payment-link.mjs
 *
 * Output（JSON）：
 *   {
 *     success: true,
 *     data: {
 *       paymentUrl: "https://m.maoyan.com/mtrade/order/list?merCode=1000545&utm_source=openclaw",
 *       description: "猫眼订单列表页面，用户可在此完成支付"
 *     }
 *   }
 */
import { run, CHANNEL_ID, UTM_SOURCE } from "./_shared.mjs";

const PAYMENT_BASE_URL = "https://m.maoyan.com/mtrade/order/list";

await run(async () => {
  const params = new URLSearchParams({
    merCode: CHANNEL_ID,
    utm_source: UTM_SOURCE,
  });
  const paymentUrl = `${PAYMENT_BASE_URL}?${params.toString()}`;

  return {
    paymentUrl,
    description: "猫眼订单列表页面，用户可在此完成支付",
  };
});
