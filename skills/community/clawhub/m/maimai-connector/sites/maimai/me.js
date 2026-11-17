/* @meta
{
  "name": "maimai/me",
  "description": "当前脉脉企业版账号信息与搜索权限自检（uid/公司/是否发布职位/是否在白名单）",
  "domain": "maimai.cn",
  "args": {},
  "capabilities": ["recruiting"],
  "readOnly": true,
  "example": "bb-browser site maimai/me"
}
*/
async function (args) {
  var UID = '<YOUR_UID>';        // 替换为你的脉脉企业版账号 uid（登录后从 maimai/me 接口或 user/current 响应中获取）
  var CO_ID = '<YOUR_CO_ID>';    // 替换为你的企业 co_id

  var me = await fetch(
    '/api/ent/user/current?channel=www&uid=' + UID + '&version=1.0.0',
    { credentials: 'include' }
  ).then(function (r) { return r.json(); });

  var pre = await fetch(
    '/api/ent/search/user_search_pre_check?channel=www&co_id=' + CO_ID + '&uid=' + UID + '&version=1.0.0',
    { credentials: 'include' }
  ).then(function (r) { return r.json(); });

  if (me.code !== 0) {
    return { error: me.error_msg || 'not logged in', hint: '脉脉登录态已失效，需重新扫码登录' };
  }

  var u = me.data.ucard || {};
  return {
    uid: u.id,
    name: u.name,
    province: u.province,
    career: u.career,
    identity: me.data.identity,
    company_id: (pre.data || {}).co_id,
    has_published_job: (pre.data || {}).has_published_job,
    in_cid_whitelist: (pre.data || {}).in_cid_whitelist,
    is_new_user: (pre.data || {}).is_new_user
  };
}
