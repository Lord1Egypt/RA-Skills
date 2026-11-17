/* @meta
{
  "name": "maimai/jobs",
  "description": "脉脉企业版在招职位列表（含薪资、城市、学历/经验要求），用于反推人才画像",
  "domain": "maimai.cn",
  "args": {
    "size": {"required": false, "description": "返回条数，默认 20"}
  },
  "capabilities": ["recruiting"],
  "readOnly": true,
  "example": "bb-browser site maimai/jobs 20"
}
*/
async function (args) {
  var UID = '<YOUR_UID>';        // 替换为你的脉脉企业版账号 uid（登录后从 maimai/me 接口或 user/current 响应中获取）
  var size = args.size || '20';

  var url = '/api/ent/job/namelist?channel=www&is_new_add=1'
    + '&size=' + encodeURIComponent(size)
    + '&uid=' + UID + '&version=1.0.0';

  var resp = await fetch(url, { credentials: 'include' });
  var j = await resp.json();

  if (!j.jobs) {
    return { error: j.error_msg || 'no jobs', hint: '登录态可能已失效，需重新扫码登录' };
  }

  return {
    count: j.jobs.length,
    jobs: j.jobs.map(function (x) {
      return {
        ejid: x.ejid,
        jid: x.jid,
        position: x.position,
        company: x.company,
        province: x.province,
        city: x.city,
        area: x.area,
        salary: x.salary,
        degree: x.degree,
        worktime: x.worktime
      };
    })
  };
}
