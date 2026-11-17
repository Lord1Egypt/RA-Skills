#!/usr/bin/env node
/** Standalone, read-only CDP capture. Requires Node 22+, no npm dependencies. */
import {readFile, writeFile} from 'node:fs/promises';
import {homedir} from 'node:os';
import {join, resolve} from 'node:path';
import {pathToFileURL} from 'node:url';

export async function dailyEndpoint(browser, {platform = process.platform, home = homedir(), localAppData = process.env.LOCALAPPDATA} = {}) {
  if (!['chrome', 'edge'].includes(browser)) throw Error('Select the customer daily browser: chrome or edge');
  const roots = platform === 'darwin'
    ? {chrome: join(home, 'Library/Application Support/Google/Chrome'), edge: join(home, 'Library/Application Support/Microsoft Edge')}
    : platform === 'win32'
      ? {chrome: join(localAppData || join(home, 'AppData/Local'), 'Google/Chrome/User Data'), edge: join(localAppData || join(home, 'AppData/Local'), 'Microsoft/Edge/User Data')}
      : {chrome: join(home, '.config/google-chrome'), edge: join(home, '.config/microsoft-edge')};
  let lines;
  try { lines = (await readFile(join(roots[browser], 'DevToolsActivePort'), 'utf8')).trim().split(/\r?\n/); }
  catch { throw Error(`Cannot find ${browser} remote-debugging endpoint. Enable remote debugging in the selected daily browser; no separate browser is started.`); }
  const port = Number(lines[0]);
  if (!Number.isInteger(port) || port < 1 || port > 65535 || !/^\/devtools\/browser(?:\/[^\s?#]+)?$/.test(lines[1] || '')) throw Error('Invalid daily-browser debugging endpoint');
  return `ws://127.0.0.1:${port}${lines[1]}`;
}

// Navigation-only helpers: data arguments are never interpolated as page code.
export const REFUSAL = /(?:enter|complete|solve) (?:the |this |a )?captcha|(?:verify|verifying|confirm) (?:that )?you are (?:a )?human|access denied|too many requests|please (?:sign|log) in|(?:sign|log) in (?:required|to continue|to view)|(?:请输入|请完成|请填写).{0,12}验证码|验证您是人类|访问受限|访问过于频繁|请先登[录入]|请按住滑块[，,\s]*拖动到最右边|为了更好的访问体验[，,\s]*请进行验证|(?:验证|确认)(?:您|你)(?:是否)?是(?:真人|人类)|(?:正在|请|需要).{0,8}(?:真人验证|人机验证)|验证成功[。.!！\s]*正在等待|verification successful[.!\s]*waiting for|checking your browser|認証が必要|ログインが必要|로그인이 필요|접근이 제한|人机验证|真人验证|请按住滑块|unusual traffic|需要进行其他验证/i;
// An unrendered body's innerText can include script/style source. Read only
// text nodes with rendered rectangles, excluding non-content elements.
export const VISIBLE_TEXT_EXPRESSION = `(() => {
  if (!document.body) return '';
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const parts = [];
  for (let node; (node = walker.nextNode());) {
    const parent = node.parentElement;
    if (!parent || parent.closest('script,style,template,noscript,[hidden],[inert]')) continue;
    const style = getComputedStyle(parent);
    if (style.visibility === 'hidden' || style.visibility === 'collapse' || style.display === 'none') continue;
    const range = document.createRange(); range.selectNodeContents(node);
    if (range.getClientRects().length && node.textContent.trim()) parts.push(node.textContent);
  }
  return parts.join('\\n');
})()`;
export const NORMAL_TEXT_EXPRESSION = `(${VISIBLE_TEXT_EXPRESSION}).replace(/\\s+/g, ' ').trim()`;
export const SNAPSHOT_EXPRESSION = `({url:location.href,title:document.title,retrieved_at:new Date().toISOString(),text:${VISIBLE_TEXT_EXPRESSION},links:[...new Set([...document.querySelectorAll('a[href]')].map(a=>a.href).filter(u=>/^https?:/.test(u)))],http_status:null})`;
export function catalogSnapshotExpression(selector) {
  const rowText = VISIBLE_TEXT_EXPRESSION.replaceAll('document.body', 'root');
  return `(() => {
    const snapshot = ${SNAPSHOT_EXPRESSION};
    const nodes = [...document.querySelectorAll(${JSON.stringify(selector)})].filter(n =>
      n.getClientRects().length && getComputedStyle(n).visibility !== 'hidden');
    if (nodes.some(n => nodes.some(other => n !== other && n.contains(other)))) throw Error('Catalog selector matches nested rows');
    snapshot.catalog_rows = nodes.map(root => {
      const raw_text = ${rowText};
      const title = raw_text.split('\\n').map(t => t.trim()).find(Boolean) || '';
      const links = [...root.querySelectorAll('a[href]')].map(a => a.href).filter(u => /^https?:/.test(u));
      if (root.matches('a[href]') && /^https?:/.test(root.href)) links.unshift(root.href);
      const url = links[0] || snapshot.url;
      return {source_id:raw_text,title,raw_text,url};
    });
    return snapshot;
  })()`;
}

export function validateBudget(budget, actionCount) {
  if (!budget || budget.version !== 1 || !Array.isArray(budget.stages) || budget.stages.length !== actionCount + 1)
    throw Error('NAVIGATION_BUDGET_REQUIRED: supply one catalog contract for the initial page and every step');
  const integer = (n, min, max) => Number.isInteger(n) && n >= min && n <= max;
  if (!integer(budget.max_rows,1,25) || !integer(budget.max_pages,1,2) || !integer(budget.used_rows,0,25) ||
      !Array.isArray(budget.used_pages) || budget.used_pages.some(n => !Number.isSafeInteger(n) || n === 0))
    throw Error('NAVIGATION_BUDGET: invalid round limits or previous usage');
  if (budget.stages.some(s => !s || !integer(s.page,1,Number.MAX_SAFE_INTEGER) || !integer(s.max_rows,0,25) ||
      !(s.row_selector === null || (typeof s.row_selector === 'string' && s.row_selector.trim())))) throw Error('NAVIGATION_BUDGET: invalid catalog contract');
  if (budget.stages.some((s,i) => s.row_selector === null && s.max_rows > 0 &&
      (i !== budget.stages.length - 1 || s.max_rows !== budget.max_rows || budget.used_rows !== 0 || budget.stages.slice(0,i).some(p=>p.max_rows))))
    throw Error('NAVIGATION_BUDGET: an unknown catalog requires a final inspection stage reserving the full unused allowance');
  const rows = budget.used_rows + budget.stages.reduce((n,s) => n + s.max_rows,0);
  const pages = new Set([...budget.used_pages,...budget.stages.filter(s=>s.max_rows>0).map(s=>s.page)]);
  if (rows > budget.max_rows || pages.size > budget.max_pages)
    throw Error(`NAVIGATION_BUDGET_EXCEEDED: planned ${rows} rows / ${pages.size} pages; split the search before connecting`);
}
export function navigationReadyExpression(text, selector = '') {
  return `Boolean((() => {
    const label = ${JSON.stringify(text)}, selector = ${JSON.stringify(selector)};
    const norm = value => (value || '').replace(/\\s+/g, ' ').trim();
    let nodes;
    try { nodes = [...document.querySelectorAll(selector || 'body *')].filter(node =>
      node.getClientRects().length && getComputedStyle(node).visibility !== 'hidden' && norm(node.innerText) === norm(label)); }
    catch { return false; }
    return nodes.filter(node => !nodes.some(other => node !== other && node.contains(other))).length === 1;
  })())`;
}

// Application, contact and account controls. A backstop for the agent's own
// read-only rule, in the languages of the markets this skill serves. Three
// layers, in order of how far each one can be trusted:
//
//   1. shape    — a catalog job title is a link; apply/contact/account controls
//                 are <button>/<input>/role="button". The page expression
//                 refuses every button-like control unless its label reads as
//                 pagination or a detail/expand control. This holds on boards
//                 whose wording nobody has seen.
//   2. anywhere — phrases that never name a job, refused wherever they occur.
//   3. whole    — verbs that also live inside job titles (删除 in 数据删除合规
//                 专员, 応募 in 応募者管理担当, ログイン, 입사지원, 로그인,
//                 "job alert" in Job Alerts Product Manager, Register, Save)
//                 are refused only as an entire control label: optional
//                 modifier/channel, verb, optional object — every object word
//                 must itself come from the object vocabulary, so a title
//                 ("Save the Children", "Message Queue Engineer") falls out.
const CN_PREFIX = '(?:请|立即|马上|立刻|现在|一键|我要|想|去|在线|点击|取消|已|快速|快捷|极速|闪电|秒|免费|确认|同意并|同意|登录后|注册后|继续|直接|开始|重新|批量)';
const CN_CHANNEL = '(?:扫码|扫一扫|微信|qq|支付宝|验证码|短信|手机号|手机|邮箱|邮件|电话|附件|在线|一键|简历|附件简历|个人简历|中文简历|英文简历|职位|岗位|工作|公司|企业|账号|账户|人才|会员|新用户)';
const CN_VERB = '(?:申请|应聘|报名|投递|投简历|发简历|递简历|投个简历|注册|登录|登入|注销|退出登录|关注|收藏|保存|分享|转发|沟通|聊天|订阅|举报|投诉|提交|发送|上传|下载|导入|填写|完善|创建|新建|添加|编辑|绑定|认证|预约|咨询|联系|私信|发消息|打招呼|加入|领取|开通|购买|支付|付款|下单|删除|撤回|撤销|评价|评论|内推|求内推)';
const CN_OBJECT = '(?:到|至|进|入)?(?:该|此|这个|我的|本|个人|附件)?(?:职位|岗位|公司|简历|企业|账号|账户|工作|面试|宣讲会|活动|参会|参展|参加|人才库|收藏夹|资料|信息|他|她|ta|hr|招聘者|招聘方|boss|老板|消息|申请|加入|一下|我们|客服|后查看|查看|投递|收藏|关注|订阅|提醒|会员|注册|登录|职位收藏)';
// Modifier and channel interleave in real labels (手机快捷登录, 一键极速投递).
const CN_LABEL = `(?:${CN_PREFIX}|${CN_CHANNEL}){0,4}${CN_VERB}${CN_OBJECT}{0,3}`;
// Verb + only object-vocabulary words. "Save job" is a control; "Save the
// Children - Program Officer" and "Share Plan Administrator" are not.
const EN_VERB = '(?:un)?(?:save|saved|follow|following|unfollow|share|report|flag|message|contact|chat|connect|email|send|interested|log ?in|login|log ?on|log ?out|sign ?out|register|purchase|buy|checkout|apply|submit|start|begin|continue|complete|finish|use|reuse|withdraw|track|create|make|set ?up|join|add|write|post|upload|attach|autofill|build|import|update|edit|manage|get|receive|enable|turn ?on|subscribe|unsubscribe|bookmark|shortlist|favou?rite|like|rate|review|refer|request|schedule|book|call|claim|redeem|delete|remove|erase)';
const EN_OBJECT = '(?:this|the|a|an|my|your|our|new|free|last|previous|saved|existing|to|for|with|now|today|later|and|on|up|via|job|jobs|role|roles|position|posting|vacancy|opening|company|employer|recruiter|hiring manager|hiring team|page|me|us|account|profile|resume|r(?:e|é)sum(?:e|é)|cv|application|applications|alert|alerts|salary|review|reviews|rating|photo|interview|question|answer|tip|favou?rite|favou?rites|shortlist|watchlist|list|collection|talent|network|community|pool|newsletter|update|updates|notification|notifications|message|messages|call|number|phone|code|password|cart|calendar|bookmark|bookmarks|wishlist|search|searches|filter|filters|friend|colleague|preference|preferences|setting|settings|subscription|subscriptions|google|apple|facebook|linkedin|github|microsoft|email|sso|apply|view|continue)';
const EN_LABEL = `${EN_VERB}(?: ${EN_OBJECT}){0,5}`;
// nl/de/fr families: apply, save, account, job alert, contact.
const EU_LABEL = [
  '(?:(?:stelle|job|vacature|offre|bedrijf|unternehmen|entreprise) )?(?:merken|volgen|delen|folgen|teilen|suivre|partager)',
  '(?:bewaar|bewaren|opslaan|sla op)(?: (?:deze|dit|de|het|je|mijn|uw))?(?: (?:vacature|vacatures|baan|job|functie|zoekopdracht|zoekactie|advertentie))?',
  '(?:reageer|reageren|solliciteer|solliciteren)(?: (?:direct|nu|op deze vacature|op deze baan))?',
  '(?:maak|maak aan|cre(?:e|ë)er|creeer|stel|instellen|ontvang|beheer)[^|]{0,24}?(?:alert|alerts|alerten|melding|meldingen|jobmelding)',
  '(?:account|profiel|profil|cv|lebenslauf|konto|benutzerkonto|nutzerkonto|compte)(?: (?:gratis|kostenlos))?(?: (?:aanmaken|maken|erstellen|anlegen|einrichten|hochladen|registrieren|l(?:o|ö)schen|cr(?:e|é)er|supprimer|upload|uploaden))',
  '(?:stuur|verstuur|verzend|schrijf)[^|]{0,20}?bericht',
  '(?:jobalarm|job-alarm|suchauftrag|suchagent|benachrichtigung|benachrichtigungen|jobagent)(?:en)?(?: (?:erstellen|einrichten|anlegen|speichern|aktivieren|abonnieren))',
  '(?:einloggen|ausloggen|kontaktieren|abonnieren|termin vereinbaren|nachricht|profil ansehen und bewerben)',
  "(?:connexion|d(?:e|\u00e9)connexion|s'identifier|identifiez-vous|se d(?:e|\u00e9)connecter|mon compte|cr(?:e|\u00e9)ez votre compte)",
  '(?:cr(?:e|é)er|recevoir|g(?:e|é)rer|modifier|supprimer)[^|]{0,28}?alerte(?:s)?(?:[^|]{0,16})?',
  '(?:contacter|contactez|joindre|envoyer)(?:\\s[^|]{0,32})?',
  '(?:postuler|candidater|je postule|sauvegarder|enregistrer|se connecter|s\'inscrire|cr(?:e|é)er un compte)(?:\\s[^|]{0,24})?',
].join('|');
// ja/ko: the verb noun plus its light verb (する / 하기), never a substring of a
// longer title (応募者管理担当, 로그인 보안 엔지니어).
const JA_LABEL = '(?:今すぐ|すぐに|かんたん|簡単|まとめて|新規|無料|この求人に|この求人を|求人を|求人に|こちらから)?(?:応募|エントリー|キープ|保存|お気に入り(?:に追加)?|会員登録|新規登録|無料登録|登録|ログイン|ログアウト|問い合わせ|お問い合わせ|連絡|メッセージ|履歴書|職務経歴書|スカウト|アカウント|プロフィール|マイページ)(?:を|に|へ)?(?:する|します|して|してください|送る|送信|申込|申し込む|追加|登録|作成|削除|保存|アップロード|受け取る)?';
const KO_LABEL = '(?:즉시|바로|간편|온라인|간단|무료|지금)?(?:입사지원|지원|스크랩|관심기업|관심|저장|찜|회원가입|가입|로그인|로그아웃|연락|문의|메시지|쪽지|이력서|채용알림|알림|스카우트)(?:\\s*(?:하기|보내기|전송|등록|첨부|설정|받기|신청|추가|삭제|제출)){0,3}';
export const ACTION_ANYWHERE = /(?:立即沟通|继续沟通|去沟通|聊一聊|聊聊|感兴趣|打招呼|投个简历|确认支付|エントリーする|気になる)|\b(?:apply|submit|sign[ -]?(?:in|up)|subscribe|unsubscribe|i(?:'m| am) interested|sollicit(?:eer|eren)|reageer|inloggen|aanmelden|registreren|opslaan|bewaren|bewerben|bewerbung|anmelden|registrieren|speichern|postuler|postulez|je postule|envoyer (?:ma|votre) candidature|candidater|se connecter|s'inscrire|sauvegarder|enregistrer|contacter|bericht (?:sturen|versturen)|neem contact op|contacteer(?: ons)?|nachricht (?:senden|schreiben)|kontakt aufnehmen|envoyer un message)\b/i;
export const ACTION_LABEL = new RegExp(`^(?:${[
  `${CN_LABEL}(?:(?:[/、·,，|]|并|且|和|与|再|然后)?${CN_LABEL}){0,2}`,
  EN_LABEL,
  'job alerts?',
  '(?:continue|sign ?in|sign ?up|log ?in|register|connect) with [^|]{1,32}',
  'continue (?:as|without) [^|]{1,24}',
  'send (?:me |my |your |us )?(?:details|detail|info(?:rmation)?|cv|resume)',
  'request (?:more |an? )?(?:info(?:rmation)?|details|call ?back|demo|quote)',
  'refer (?:a |an )?(?:friend|colleague|candidate|someone)',
  'get (?:notified|alerts?|job alerts?|hired|started)',
  EU_LABEL,
  // es/pt/it/pl: outside the markets this skill serves, but cheap to refuse.
  '(?:inscribirse|inscr(?:i|í)bete|postularse|postular|postule-se|candidatar-se|candidate-se|aplicar|aplique|solicitar|enviar (?:mi |meu |o )?(?:cv|curr(?:i|í)cul(?:o|um)|candidatura)|iniciar sesi(?:o|ó)n|crear (?:una )?cuenta|criar conta|guardar|salvar vaga|aplikuj|zaloguj si(?:e|ę)|zapisz|utw(?:o|ó)rz konto|candidati|invia candidatura|accedi|registrati)(?:\\s[^|]{0,20})?',
  JA_LABEL,
  KO_LABEL,
].join('|')})$`, 'i');
// Read-only vocabulary: the only labels a button-like control may carry.
// Consulted after the refusal lists, so an action word can never be read here.
export const SAFE_NAVIGATION = new RegExp(`^(?:${[
  '\\d{1,4}',
  '第\\s*\\d{1,4}\\s*[页頁]', '共\\s*\\d{1,4}\\s*[页頁]', '[上下]一?[页頁]', '[首末尾][页頁]',
  '(?:go to )?(?:next|previous|prev|first|last)(?: (?:page|results?|jobs?|set))?', 'page \\d{1,4}',
  '(?:load|show|see|view) more(?: (?:jobs|results|details))?',
  'volgende(?: pagina)?', 'vorige(?: pagina)?', '(?:eerste|laatste)(?: pagina)?',
  'n(?:ä|ae)chste[sr]?(?: seite)?', 'vorherige(?: seite)?', 'weiter', 'zur(?:ü|ue)ck', '(?:erste|letzte) seite',
  '(?:page )?suivante?', '(?:page )?pr(?:é|e)c(?:é|e)dente?', '(?:premi|derni)(?:è|e)re page',
  '次(?:へ|のページ)?', '前(?:へ|のページ)?', '(?:最初|最後)のページ',
  '다음(?:\\s*페이지)?', '이전(?:\\s*페이지)?', '처음', '마지막',
  '(?:查看|職位|职位|岗位|崗位|工作)?[详詳][情细細]', '[详詳][细細](?:信息|資訊)',
  '查看更多', '更多(?:信息|职位|内容)?', '加载更多', '展[开開]', '收起', '[显顯]示更多', '查看全文', '[阅閱]读全文', '全文',
  '(?:view |see |show |read )?details?', 'job details?', 'view (?:job|more|full description|description)',
  '(?:read|see) (?:more|full description)', 'show (?:more|less|full description)', 'more(?: info(?:rmation)?)?',
  'full (?:job )?description', 'expand', 'collapse', 'learn more', 'quick view', 'preview',
  '(?:bekijk |toon |lees )?(?:details|meer|vacature|functieomschrijving)', 'meer (?:tonen|lezen|informatie|details)',
  'mehr(?: (?:anzeigen|erfahren|lesen|details))?', 'details anzeigen', 'weitere details', '(?:aus|ein)klappen', 'stellenbeschreibung',
  'plus', 'voir (?:plus|les d(?:é|e)tails|le d(?:é|e)tail)', 'en savoir plus', 'lire la suite', 'afficher plus', 'd(?:é|e)tails?',
  '詳細(?:を見る)?', 'もっと見る', '続きを読む', 'さらに表示', '全文を読む',
  '상세(?:보기)?', '자세히(?:\\s*보기)?', '더\\s*보기', '전체\\s*보기', '공고\\s*보기',
].join('|')})$`, 'i');
// A pager rendered as a glyph alone. Checked before punctuation is trimmed.
export const PAGINATION_GLYPH = /^[\s«»‹›<>〈〉⟨⟩→←⇒⇐▶◀▸◂]+$/;
// Full-width letters, curly apostrophes and a space typed inside a CJK button
// label must not dodge the lists above.
export function normalizeActionLabel(label, keepEdgePunctuation) {
  const text = String(label || '').normalize('NFKC').replace(/[‘’ʼ`´]/g, "'")
    .replace(/\s+/g, ' ').trim()
    .replace(/([\p{sc=Han}\p{sc=Hiragana}\p{sc=Katakana}\p{sc=Hangul}]) (?=[\p{sc=Han}\p{sc=Hiragana}\p{sc=Katakana}\p{sc=Hangul}])/gu, '$1');
  return keepEdgePunctuation ? text : text.replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, '');
}
export function isActionControl(label) {
  const text = normalizeActionLabel(label);
  return ACTION_ANYWHERE.test(text) || ACTION_LABEL.test(text);
}
// Pagination or a detail/expand control: the read-only vocabulary that lets a
// button-like control through the structural refusal.
export function isSafeNavigationLabel(label) {
  const text = normalizeActionLabel(label);
  return (text !== '' && SAFE_NAVIGATION.test(text)) || PAGINATION_GLYPH.test(normalizeActionLabel(label, true));
}
export function clickExpression(text, selector = '') {
  return `(() => {
    const label = ${JSON.stringify(text)}, selector = ${JSON.stringify(selector)};
    const norm = value => (value || '').replace(/\\s+/g, ' ').trim();
    const visible = node => Boolean(node.getClientRects().length) && getComputedStyle(node).visibility !== 'hidden';
    const anywhere = new RegExp(${JSON.stringify(ACTION_ANYWHERE.source)}, ${JSON.stringify(ACTION_ANYWHERE.flags)});
    const whole = new RegExp(${JSON.stringify(ACTION_LABEL.source)}, ${JSON.stringify(ACTION_LABEL.flags)});
    const safe = new RegExp(${JSON.stringify(SAFE_NAVIGATION.source)}, ${JSON.stringify(SAFE_NAVIGATION.flags)});
    const glyph = new RegExp(${JSON.stringify(PAGINATION_GLYPH.source)}, ${JSON.stringify(PAGINATION_GLYPH.flags)});
    const normalizeActionLabel = ${normalizeActionLabel.toString()};
    const forbidden = {test: value => {const t = normalizeActionLabel(value); return anywhere.test(t) || whole.test(t);}};
    const readOnlyLabel = {test: value => {const t = normalizeActionLabel(value); return (t !== '' && safe.test(t)) || glyph.test(normalizeActionLabel(value, true));}};
    // Upstream exception: an observed catalog filter button.
    const filterLabel = Boolean(selector) && /^apply (?:all )?filters$/i.test(norm(label));
    if (forbidden.test(label) && !filterLabel) return {error:'Only read-only job/detail/pagination navigation is allowed'};
    let nodes;
    try {nodes = [...document.querySelectorAll(selector || 'body *')].filter(n => visible(n) && norm(n.innerText) === norm(label));}
    catch {return {error:'Invalid click selector'};}
    nodes = nodes.filter(n => !nodes.some(other => n !== other && n.contains(other)));
    if (nodes.length !== 1) return {error:'Navigation label must identify exactly one visible element; use an observed selector'};
    const node = nodes[0], control = node.closest('a,button,input,[role="button"]') || node;
    const filterButton = filterLabel && control.tagName === 'BUTTON' && norm(control.innerText) === norm(label);
    const controlLabel = norm(control.innerText) || norm(control.value) || norm(control.getAttribute('value')) || norm(label);
    if ((filterLabel && !filterButton) || control.disabled || control.getAttribute('aria-disabled') === 'true' || control.closest('form') || (forbidden.test(controlLabel) && !filterButton)) return {error:'Refusing a form, disabled, or account/application control'};
    // Structure over vocabulary: a catalog job title is a link, while apply,
    // contact and account controls are buttons. A button-like control is
    // refused unless it reads as pagination or a detail/expand control, so an
    // unseen board's wording cannot talk its way into an irreversible click.
    const role = (control.getAttribute('role') || '').toLowerCase();
    if (!filterButton && (['BUTTON', 'INPUT'].includes(control.tagName) || role === 'button') && !readOnlyLabel.test(controlLabel)) {
      return {error:'Refusing a button-like control: only pagination and detail/expand buttons are read-only navigation. Use the job title link, or an observed --click-selector for the link itself.'};
    }
    const href = control.getAttribute('href');
    const inert = /^javascript:\\s*void\\s*\\(\\s*0\\s*\\)\\s*;?$/i.test(href || '');
    if (href && !inert && !/^(?:https?:|#|\\/|\\.|[^:]+$)/i.test(href)) return {error:'Refusing a non-navigation link'};
    // Keep popup-style job links inside the one task-owned tab. No submission
    // default action is allowed; explicit controls were checked above.
    document.addEventListener('submit', event => {event.preventDefault();event.stopImmediatePropagation();}, true);
    window.open = next => {const target = new URL(next, location.href);if (!['http:', 'https:'].includes(target.protocol) || target.username || target.password) throw Error('Invalid navigation URL');location.assign(target.href);return window;};
    if (control.tagName === 'A') control.target = '_self';
    node.click();
    return {performed:true,label,selector,action:'navigate',clicked_at:new Date().toISOString()};
  })()`;
}

export async function capture({endpoint, url, settleMs = 1500, timeoutMs = 15000, waitStagesMs = [timeoutMs, timeoutMs * 2, timeoutMs * 4], waitForText = '', revealSelector = '', clickText = '', clickSelector = '', inspectText = '', steps = [], budget = null, WebSocketImpl = globalThis.WebSocket}) {
  if (clickSelector && !clickText) throw Error('--click-selector requires --click-text');
  if (!Array.isArray(steps) || steps.length > 8 || steps.some(step =>
      !step || typeof step.text !== 'string' || !step.text.trim() ||
      (step.selector !== undefined && typeof step.selector !== 'string'))) throw Error('Use at most eight observed navigation steps');
  if (steps.length && (clickText || clickSelector)) throw Error('Use steps or a single click, not both');
  const actions = steps.length ? steps : clickText ? [{text:clickText, selector:clickSelector}] : [];
  if (actions.length || budget) validateBudget(budget, actions.length);
  const targetUrl = new URL(url);
  if (!['http:', 'https:'].includes(targetUrl.protocol) || targetUrl.username || targetUrl.password) throw Error('Capture URL must be HTTP(S), without credentials');
  const socketUrl = new URL(endpoint);
  if (!['ws:', 'wss:'].includes(socketUrl.protocol) || !socketUrl.pathname.startsWith('/devtools/browser')) throw Error('Use a browser-level CDP WebSocket endpoint');
  if (!WebSocketImpl) throw Error('Node 22+ is required for the built-in CDP reader');
  const ws = new WebSocketImpl(endpoint);
  let seq = 0, sessionId, targetId, frameId, handedOff = false;
  const pending = new Map(), responses = [], trace = [];
  function send(method, params = {}, session = sessionId, deadline = timeoutMs) {
    return new Promise((ok, fail) => {
      const id = ++seq;
      const timer = setTimeout(() => { pending.delete(id); fail(Error(`CDP timeout: ${method}`)); }, deadline);
      pending.set(id, {ok, fail, timer});
      const command = {id, method, params};
      if (session) command.sessionId = session;
      trace.push({method, targetId: targetId || null, sessionId: session || null});
      try { ws.send(JSON.stringify(command)); } catch (err) {clearTimeout(timer);pending.delete(id);fail(err);}
    });
  }
  ws.addEventListener('message', event => {
    let msg; try { msg = JSON.parse(event.data); } catch {return;}
    const item = pending.get(msg.id);
    if (item) { clearTimeout(item.timer);pending.delete(msg.id);msg.error ? item.fail(Error(msg.error.message)) : item.ok(msg.result); }
    if (msg.sessionId === sessionId && msg.method === 'Network.responseReceived' && msg.params.type === 'Document') responses.push(msg.params);
  });
  ws.addEventListener('close', () => {
    for (const p of pending.values()) {clearTimeout(p.timer);p.fail(Error('CDP connection closed'));} pending.clear();
  });
  try {
    await new Promise((ok, fail) => {
      const timer = setTimeout(() => fail(Error('CDP connection timeout; check browser connection consent')), timeoutMs);
      ws.addEventListener('open', () => {clearTimeout(timer);ok();}, {once:true});
      ws.addEventListener('error', () => {clearTimeout(timer);fail(Error('CDP connection failed'));}, {once:true});
    });
    ({targetId} = await send('Target.createTarget', {url:'about:blank', background:true}));
    if (!targetId) throw Error('CDP did not create a task-owned tab');
    ({sessionId} = await send('Target.attachToTarget', {targetId, flatten:true}));
    if (!sessionId) throw Error('CDP did not attach the task-owned tab');
    await send('Page.enable');await send('Network.enable');
    const navigation = await send('Page.navigate', {url});
    frameId = navigation.frameId;
    if (navigation.errorText) throw Error(`Navigation failed: ${navigation.errorText}`);
    let ready = false, refused = false;
    const renderWaits = [];
    const reveal = revealSelector ? {selector:revealSelector, performed:false} : null;
    const waitForPage = async (expectedText, action = null) => {
      ready = false;refused = false;
      for (const waitMs of waitStagesMs) {
        renderWaits.push(waitMs);
        const deadline = Date.now() + waitMs;
        // do/while, not while: a stage whose budget is already spent when it
        // starts must still CHECK once. As `while`, a short stage could run
        // zero iterations, leave `refused` false and report no refusal at all —
        // a 403 the page really served, silently dropped. Production stages are
        // 15s and never hit it; two concurrent `node --test` processes did, and
        // turned CI red on a commit that had passed minutes earlier.
        do {
          refused = responses.some(x => x.frameId === frameId && [401, 403, 429].includes(x.response.status));
          if (refused) break;
          const r = await send('Runtime.evaluate', {expression:'document.readyState', returnByValue:true});
          if (r.result?.value === 'complete') {
            const content = expectedText ? await send('Runtime.evaluate', {
              expression:action ? navigationReadyExpression(action.text, action.selector || '') : `Boolean(${NORMAL_TEXT_EXPRESSION}.includes(${JSON.stringify(expectedText.replace(/\s+/g, ' ').trim())}))`, returnByValue:true,
            }) : null;
            if (!expectedText || content.result?.value === true) {ready = true;break;}
            // A complete SPA can have redirected to login while the requested
            // detail heading remains absent. Do not wait through all three stages.
            const wallNow = await send('Runtime.evaluate', {
              expression:`Boolean(${REFUSAL.toString()}.test(${NORMAL_TEXT_EXPRESSION}))`, returnByValue:true,
          });
          if (wallNow.result?.value === true) {refused = true;break;}
          }
          if (Date.now() >= deadline) break;
          await new Promise(r => setTimeout(r, Math.max(1, Math.min(250, deadline - Date.now()))));
        } while (Date.now() < deadline);
        if (ready || refused) break;
        // Inspect a stalled page before waiting longer; never wait through a
        // known human-verification wall merely because its load event is pending.
        const wall = await send('Runtime.evaluate', {expression:`Boolean(
          (/(^|\\.)zhipin\\.com$/.test(location.hostname) && location.pathname === '/web/passport/zp/security.html') ||
          ${REFUSAL.toString()}.test(${NORMAL_TEXT_EXPRESSION}) ||
          /(?:您|你)所在的(?:用户组|用戶組)\\s*[（(]\\s*(?:游客|遊客)\\s*[)）]\\s*(?:无法|無法|不能)(?:进行|進行)此操作/.test(${NORMAL_TEXT_EXPRESSION})
        )`, returnByValue:true});
        refused = wall.result?.value === true;
        if (refused) break;
        // Only reveal an observed lazy-loaded node after the first background
        // wait. Activation is restricted to the tab this capture created.
        if (reveal && renderWaits.length === 1) {
          const selector = JSON.stringify(revealSelector);
          const found = await send('Runtime.evaluate', {
            expression:`Boolean(document.querySelector(${selector}))`, returnByValue:true,
          });
          if (found.exceptionDetails) throw Error('Invalid reveal selector');
          if (found.result?.value !== true) throw Error(`Reveal selector not found: ${revealSelector}`);
          await send('Target.activateTarget', {targetId}, null);
          if (settleMs) await new Promise(r => setTimeout(r, settleMs));
          const scrolled = await send('Runtime.evaluate', {
            expression:`(() => {const node = document.querySelector(${selector}); if (!node) return false; node.scrollIntoView({block:'center',behavior:'instant'}); return true;})()`, returnByValue:true,
          });
          if (scrolled.exceptionDetails || scrolled.result?.value !== true) throw Error('Could not reveal the requested page node');
          reveal.performed = true;
          reveal.after_wait_stage = renderWaits.length;
          reveal.revealed_at = new Date().toISOString();
        }
      }
    };
    await waitForPage(actions[0]?.text || waitForText, actions[0]);
    let navigationAction = null;
    const navigationSteps = [];
    const stages = [];
    let budgetExceeded = false, currentSnapshot = null, navigationError = null;
    const readSnapshot = async index => {
      const plan = budget?.stages[index];
      const r = await send('Runtime.evaluate', {expression:plan?.row_selector ? catalogSnapshotExpression(plan.row_selector) : SNAPSHOT_EXPRESSION, returnByValue:true});
      if (r.exceptionDetails || !r.result?.value?.url) throw Error('Could not read the page snapshot/catalog selector');
      const value = r.result.value;
      const response = responses.filter(x => x.frameId === frameId && x.response.url === value.url).at(-1);
      value.http_status = response?.response.status ?? null;
      if (plan) {
        if (plan.row_selector === null) {
          value.catalog_rows = [];
          if (plan.max_rows > 0) value.catalog_accounting_pending = true;
        }
        if (!Array.isArray(value.catalog_rows)) throw Error('Catalog capture omitted DOM rows');
        // Preserve a refusal but do not extract cards from an interstitial.
        if (refused || value.http_status >= 400 || REFUSAL.test(value.text.replace(/\s+/g,' '))) {
          value.catalog_rows = [];
          delete value.catalog_accounting_pending;
          if (refused) value.blocked = true;
        }
        stages.push({...plan,row_count:value.catalog_accounting_pending ? null : value.catalog_rows.length});
        budgetExceeded ||= value.catalog_rows.length > plan.max_rows;
      }
      return value;
    };
    if (budget) currentSnapshot = await readSnapshot(0);
    for (const [index, action] of actions.entries()) {
      if (refused || budgetExceeded || !ready || currentSnapshot?.catalog_accounting_pending || currentSnapshot?.http_status >= 400) break;
      // Check the actual page even when readyState completed before the first
      // retry. A ready login/captcha page is not permission to interact.
      const source = currentSnapshot || await readSnapshot(index);
      if (!source) throw Error('Could not inspect page before navigation');
      if (REFUSAL.test(source.text.replace(/\s+/g, ' '))) refused = true;
      else try {
        const clicked = await send('Runtime.evaluate', {expression:clickExpression(action.text, action.selector || ''), returnByValue:true});
        if (clicked.exceptionDetails || !clicked.result?.value?.performed) throw Error(clicked.result?.value?.error || 'Could not activate the requested navigation');
        navigationAction = {...clicked.result.value, source_url:source.url, source_text:source.text, source_links:source.links, source_snapshot:source};
        if (settleMs) await new Promise(r => setTimeout(r, settleMs));
        await waitForPage(actions[index + 1]?.text || waitForText, actions[index + 1]);
        currentSnapshot = await readSnapshot(index + 1);
        navigationAction.result = currentSnapshot;
        navigationSteps.push(navigationAction);
        if (REFUSAL.test(currentSnapshot.text.replace(/\s+/g, ' '))) refused = true;
      } catch (error) {
        // A failed later click/read must not erase the catalogs already read.
        navigationError = {step:index + 1, text:action.text, message:error.message};
        break;
      }
    }
    // Ads and other resources can keep a readable page from reaching complete.
    // Preserve the actual DOM and refusal status at the deadline for diagnosis.
    if (!budget && settleMs) await new Promise(r => setTimeout(r, settleMs));
    const snapshot = {...(currentSnapshot || await readSnapshot(0))};
    snapshot.requested_url = url;
    if (inspectText) {
      const inspected = await send('Runtime.evaluate', {expression:`(() => {
        const label = ${JSON.stringify(inspectText)};
        const found = [...document.querySelectorAll('body *')].filter(n => n.getClientRects().length && n.innerText?.trim() === label);
        return found.filter(n => !found.some(other => n !== other && n.contains(other))).slice(0,5).map(n => {
          const ancestors=[];let parent=n.parentElement;
          for(let i=0;parent && parent!==document.body && i<3;i++,parent=parent.parentElement)
            ancestors.push({html:parent.outerHTML.slice(0,12000),truncated:parent.outerHTML.length>12000});
          return {text:n.innerText,parent_html:n.parentElement.outerHTML.slice(0,12000),truncated:n.parentElement.outerHTML.length>12000,ancestors};
        });
      })()`, returnByValue:true});
      if (inspected.exceptionDetails) throw Error('Could not inspect the requested navigation label');
      snapshot.inspected_nodes = inspected.result?.value || [];
    }
    if (navigationSteps.length) snapshot.navigation = navigationSteps.at(-1);
    if (navigationSteps.length) snapshot.navigation_steps = navigationSteps;
    if (budget) {
      snapshot.navigation_budget = {...budget,stages,observed_rows:stages.some(s=>s.row_count===null) ? null : stages.reduce((n,s)=>n+s.row_count,0),
        observed_pages:[...new Set(stages.filter(s=>s.row_count>0).map(s=>s.page))].sort((a,b)=>a-b)};
      if (budgetExceeded) snapshot.budget_exceeded = true;
    }
    if (navigationError) snapshot.navigation_error = navigationError;
    if (REFUSAL.test(snapshot.text.replace(/\s+/g, ' '))) refused = true;
    if (refused) snapshot.blocked = true;
    snapshot.load_timed_out = !ready && !refused;
    snapshot.render_wait_budgets_ms = renderWaits;
    if (waitForText) snapshot.wait_for_text = waitForText;
    if (reveal) snapshot.reveal = reveal;
    const response = responses.filter(x => x.frameId === frameId && x.response.url === snapshot.url).at(-1);
    snapshot.http_status = response?.response.status ?? null;
    snapshot.capture = {backend:'builtin-cdp', targetId, trace};
    if (refused || [401,403,429].includes(snapshot.http_status)) {
      // Keep the exact page and its login/challenge state, not a reopened URL.
      // The session broker releases ownership before activating the tab.
      handedOff = true;
      try {
        await send('JobHunt.handoffTarget', {targetId}, null);
      } catch (error) {
        if (!/(?:wasn't found|method not found|unknown method|-32601)/i.test(error.message)) throw error;
        // Direct browser-level CDP has no cleanup broker; detach is enough.
        await send('Target.activateTarget', {targetId}, null);
        await send('Target.detachFromTarget', {sessionId}, null);
      }
      snapshot.handoff = {required:true,targetId,kept_open:true,reason:'user_action_required'};
    }
    return snapshot;
  } finally {
    try {
      if (targetId && !handedOff && ws.readyState === 1) {
        const result = await send('Target.closeTarget', {targetId}, null, 3000);
        if (!result.success) throw Error('CDP did not confirm closing the task-owned tab');
      }
    } finally {ws.close();}
  }
}

export async function main(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--help') {console.log('node scripts/browser_cdp.mjs --browser chrome|edge --url URL --output raw/site-capture.json [--wait-for-text "Expected description heading"] [--reveal-selector "Observed lazy-loaded node selector"] [--click-text "Exact observed job title or navigation label"] [--click-selector "Observed selector for an ambiguous label"] [--inspect-text "Observed label to inspect"] [--steps-file observed-navigation.json] [--budget-file wrapper-generated.json; use run_tool.py --workspace WS --site SITE --budget-plan PLAN for navigation] [--endpoint ws://.../devtools/browser/...]');return;}
    if (!['--browser','--url','--output','--endpoint','--wait-for-text','--reveal-selector','--click-text','--click-selector','--inspect-text','--steps-file','--budget-file'].includes(argv[i]) || !argv[i+1]) throw Error(`Unknown or incomplete argument: ${argv[i]}`);
    args[argv[i].slice(2)] = argv[++i];
  }
  if (!args.url || !args.output) throw Error('--url and --output are required');
  const endpoint = args.endpoint || await dailyEndpoint(args.browser);
  const snapshot = await capture({endpoint, url:args.url, waitForText:args['wait-for-text'] || '', revealSelector:args['reveal-selector'] || '', clickText:args['click-text'] || '', clickSelector:args['click-selector'] || '', inspectText:args['inspect-text'] || '', steps:args['steps-file'] ? JSON.parse(await readFile(args['steps-file'], 'utf8')) : [], budget:args['budget-file'] ? JSON.parse(await readFile(args['budget-file'], 'utf8')) : null});
  await writeFile(args.output, JSON.stringify(snapshot, null, 2), {flag:'wx'});
  console.log(JSON.stringify({output:args.output, url:snapshot.url, http_status:snapshot.http_status, characters:snapshot.text.length, backend:'builtin-cdp'}));
  if (snapshot.budget_exceeded || snapshot.navigation_error || snapshot.catalog_accounting_pending) process.exitCode = 2;
}
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  main(process.argv.slice(2)).catch(err => {console.error(err.message);process.exitCode=1;});
}
