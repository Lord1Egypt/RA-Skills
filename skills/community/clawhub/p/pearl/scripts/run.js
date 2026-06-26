import { loadConfig, loadPending, savePending, removePending } from './io.js';

function validateSkillUrl(raw) {
  const u = new URL(raw);
  if (u.protocol !== 'https:') throw new Error(`skill URLs must use https — got ${u.protocol}`);
  const h = u.hostname;
  if (h === 'localhost' || /^[\d.:]+$/.test(h) || /^[\da-f:]+$/i.test(h))
    throw new Error(`IP addresses not allowed — use a domain name: ${h}`);
}

export async function run(slug, url) {
  if (!/^[a-z0-9_-]+$/.test(slug)) {
    throw new Error(`invalid skill slug: ${slug}`);
  }
  validateSkillUrl(url);
  const config = loadConfig();
  if (!config.skill_token) {
    throw new Error('skill_token missing from ~/.pearl/config.json — re-run setup to upgrade.');
  }

  let chargeId = null;
  const pending = loadPending(slug);
  if (pending) {
    chargeId = pending.charge_id;
  }

  const target = chargeId ? `${url}${url.includes('?') ? '&' : '?'}charge_id=${chargeId}` : url;
  const res = await fetch(target, { headers: { Authorization: `Bearer ${config.skill_token}` }, redirect: 'error' });

  if (res.status === 200) {
    removePending(slug);
    return await res.text();
  }

  if (res.status === 202) {
    const body = await res.json();
    if (body.charge_id) {
      savePending(slug, { charge_id: body.charge_id });
      console.log('Approval needed. Ask user to approve the charge in the Pearl dashboard, then run this command again.');
    } else {
      console.log(body.message || 'Still awaiting approval.');
    }
    return;
  }

  removePending(slug);
  throw new Error(`Pearl API error (${res.status}): ${await res.text()}`);
}
