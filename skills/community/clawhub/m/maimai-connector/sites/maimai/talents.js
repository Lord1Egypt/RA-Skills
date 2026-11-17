/* @meta
{
  "name": "maimai/talents",
  "description": "脉脉企业版人才列表（人才银行/推荐位），返回候选人姓名、公司、职位、活跃度与主页链接",
  "domain": "maimai.cn",
  "args": {
    "page": {"required": false, "description": "页码，从 0 开始，默认 0"},
    "size": {"required": false, "description": "每页条数，默认 20，最大 50"},
    "project_id": {"required": false, "description": "职位项目 ID，留空为全部人才库"}
  },
  "capabilities": ["search", "recruiting"],
  "readOnly": true,
  "example": "bb-browser site maimai/talents 0 20"
}
*/
/* 脉脉企业版 /api/ent/* 接口的硬约束（实测得出，改动前务必确认）：
   1. 必须带 uid=<当前账号 uid>，否则返回 21001 "Incorrect parameters"；
   2. 认证靠浏览器登录态（扫码登录后下发的 session cookie），不在 header 里传 token；
   3. 登录态会过期，失效时接口返回 20002/21001，需重新扫码。
*/
async function (args) {
  var UID = '<YOUR_UID>';        // 替换为你的脉脉企业版账号 uid（登录后从 maimai/me 接口或 user/current 响应中获取）
  var page = args.page || '0';
  var size = args.size || '20';
  var pid = args.project_id || '';

  var url = '/api/ent/project/talent/recommendation'
    + '?channel=www&data_version=4.1'
    + '&page=' + encodeURIComponent(page)
    + '&project_id=' + encodeURIComponent(pid)
    + '&size=' + encodeURIComponent(size)
    + '&uid=' + UID + '&version=1.0.0';

  var resp = await fetch(url, { credentials: 'include' });
  var j = await resp.json();

  if (j.code !== 0) {
    return {
      error: j.error_msg || ('error_code ' + j.error_code),
      hint: '脉脉登录态可能已失效，需要重新扫码登录'
    };
  }

  var list = (j.data && j.data.list) || [];
  return {
    total: j.data.total,
    count: list.length,
    page: Number(page),
    talents: list.map(function (t) {
      return {
        id: t.id,
        name: t.name,
        gender: t.gender_str || '',
        company: t.company,
        position: t.position,
        city: t.city || t.ht_city || '',
        active: t.active_state || '',
        viewed: t.viewed,
        url: t.detail_url
      };
    })
  };
}
