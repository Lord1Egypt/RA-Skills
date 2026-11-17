export function entities(value){return String(value).replace(/&(#x[0-9a-f]+|#\d+|amp|lt|gt|quot|apos|nbsp);/gi,(_,key)=>{if(key[0]!=='#')return ({amp:'&',lt:'<',gt:'>',quot:'"',apos:"'",nbsp:' '})[key.toLowerCase()];const n=key[1].toLowerCase()==='x'?parseInt(key.slice(2),16):parseInt(key.slice(1),10);return n>0&&n<=0x10ffff&&!(n>=0xd800&&n<=0xdfff)?String.fromCodePoint(n):'';});}
export function plain(value,max=24000){return Array.from(entities(value.replace(/<(script|style|noscript|template)\b[^>]*>[\s\S]*?<\/\1\s*>/gi,' ').replace(/<[^>]*>/g,' ')).replace(/[\u0000-\u001f\u007f]/g,' ').replace(/\s+/g,' ').trim()).slice(0,max).join('');}
function attrs(tag){const out={};for(const m of tag.matchAll(/([A-Za-z_:][\w:.-]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>=]+))/g))out[m[1].toLowerCase()]=entities(m[2]??m[3]??m[4]);return out;}
export function pageMetadata(html){
 const meta={},links=[];for(const m of html.matchAll(/<(?:meta|link)\b(?:[^>"']|"[^"]*"|'[^']*')*>/gi)){
  const a=attrs(m[0]);if(/^<meta/i.test(m[0])){const key=(a.name||a.property||'').toLowerCase();if(key&&!Object.hasOwn(meta,key))meta[key]=plain(a.content||'',1200);}else links.push(a);
 }
 const title=/<title\b[^>]*>([\s\S]*?)<\/title\s*>/i.exec(html);
 return {title:title?plain(title[1],300):'',description:meta.description||'',robots:meta.robots||'',canonical:links.find(x=>(x.rel||'').toLowerCase().split(/\s+/).includes('canonical'))?.href||'',publishedRaw:meta['article:published_time']||meta['datepublished']||meta['date']||''};
}
export function articleText(html){const main=/<(?:article|main)\b[^>]*>([\s\S]*?)<\/(?:article|main)\s*>/i.exec(html);return plain(main?main[1]:html,24000);}
