/**
 * 麦当劳MCP API调用脚本
 * 使用方法: node mcdonalds-mcp.js <token> <method> [params]
 * 
 * 示例:
 * node mcdonalds-mcp.js YOUR_TOKEN get_product_list
 * node mcdonalds-mcp.js YOUR_TOKEN get_coupons
 * node mcdonalds-mcp.js YOUR_TOKEN create_order '{"productId": "xxx", "addressId": "xxx"}'
 */

const MCP_BASE_URL = 'https://mcp.mcd.cn';

const MCP_METHODS = {
  // 点餐
  get_product_list: 'food/getProductList',
  get_product_detail: 'food/getProductDetail',
  get_address_list: 'food/getAddressList',
  add_address: 'food/addAddress',
  get_coupons: 'food/getCoupons',
  calculate_price: 'food/calculatePrice',
  create_order: 'food/createOrder',
  get_order_detail: 'food/getOrderDetail',
  
  // 麦麦日历
  get_calendar: 'calendar/query',
  
  // 麦麦省
  get_coupon_list: 'coupon/getList',
  receive_coupon: 'coupon/receive',
  my_coupons: 'coupon/myCoupons',
  
  // 麦麦商城
  get_points: 'points/myPoints',
  get_exchange_list: 'points/exchangeList',
  get_exchange_detail: 'points/exchangeDetail',
  create_exchange_order: 'points/createOrder',
  
  // 通用
  get_time: 'common/getTime'
};

async function callMCP(token, method, params = {}) {
  const endpoint = MCP_METHODS[method];
  if (!endpoint) {
    console.error(`未知方法: ${method}`);
    console.log('可用方法:', Object.keys(MCP_METHODS).join(', '));
    process.exit(1);
  }
  
  const response = await fetch(`${MCP_BASE_URL}/${endpoint}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(params)
  });
  
  const result = await response.json();
  console.log(JSON.stringify(result, null, 2));
  return result;
}

// CLI入口
const [,, token, method, paramsStr] = process.argv;

if (!token || !method) {
  console.log(`
麦当劳MCP API调用脚本

用法: node mcdonalds-mcp.js <token> <method> [params]

方法列表:
${Object.entries(MCP_METHODS).map(([k, v]) => `  ${k} - ${v}`).join('\n')}

示例:
  node mcdonalds-mcp.js YOUR_TOKEN get_product_list
  node mcdonalds-mcp.js YOUR_TOKEN get_coupons
  node mcdonalds-mcp.js YOUR_TOKEN get_address_list
  `);
  process.exit(1);
}

const params = paramsStr ? JSON.parse(paramsStr) : {};
callMCP(token, method, params).catch(console.error);
