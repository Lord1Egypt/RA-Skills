/* Shared standalone HTML builder for the website and the portable skill runtime. */
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),read=file=>fs.readFileSync(path.join(root,file),'utf8');
let cached;
function resources(){
 if(cached)return cached;
 let fontCSS='',webFontCSS='';
 for(const [file,family] of [['elegant','Atlas Elegant'],['business','Atlas Business'],['brush','Atlas Brush'],['playful','Atlas Playful'],['wenkai','Atlas WenKai'],['inter','Atlas Inter'],['lora','Atlas Lora'],['jetbrains','Atlas JetBrains'],['excalifont','Atlas Excali']]){
  const data=fs.readFileSync(path.join(root,'assets/fonts',file+'.woff2')).toString('base64');
  fontCSS+=`/* ${family}\n${read('assets/fonts/'+file+'-OFL.txt').replace(/\*\//g,'* /')} */\n@font-face{font-family:'${family}';src:url(data:font/woff2;base64,${data}) format('woff2');font-weight:400;font-display:swap;}`;
  webFontCSS+=`/* ${family}\n${read('assets/fonts/'+file+'-OFL.txt').replace(/\*\//g,'* /')} */\n@font-face{font-family:'${family}';src:url(fonts/${file}.woff2) format('woff2');font-weight:400;font-display:swap;}`;
 }
 cached={license:read('LICENSE'),template:read('src/index.html'),player:read('src/player.template.html'),playerCSS:fontCSS+read('src/player.css'),playerApp:['doodle.cjs','fusheng.cjs','render.cjs','media.cjs','player.js'].map(f=>read('src/'+f)).join('\n'),css:fontCSS+read('src/styles.css')+read('src/site.css'),webCSS:webFontCSS+read('src/styles.css')+read('src/site.css'),library:read('src/library.cjs'),engine:['hierarchy.cjs','engine.cjs','edit.cjs'].map(f=>read('src/'+f)).join('\n'),app:['doodle.cjs','fusheng.cjs','render.cjs','picker.cjs','reader-export.cjs','app.js','landing.cjs'].map(f=>read('src/'+f)).join('\n')};return cached;
}
function generate(boot,options={}){
 if(boot.document){const model=require('./edit.cjs').create(boot);boot={...boot,document:model.document(),source:model.markdown(boot.recipeCode)};}
 const r=resources(),script=JSON.stringify(boot).replace(/</g,'\\u003c');
 let playerCSS=r.playerCSS;
 if(boot.player&&!options.allPlayerFonts)playerCSS=require('./reader-export.cjs').fonts(playerCSS,boot);
 const base=(boot.player?r.player:r.template).replace(/<script id="source-preview">[\s\S]*?<\/script>/,'');
 const template=boot.standalone?base.replace(/<title>[\s\S]*?<\/title>/,()=>'<title>'+require('./engine.cjs').escapeXML(require('./engine.cjs').parseMindmap(boot.source).text)+' · mindbox</title>'):base;
 return template.replace('<head>',()=>'<head>\n<!-- Mindbox engine license (does not license user content):\n'+r.license.replace(/--/g,'- -')+'\n-->').replace('/*__CSS__*/',()=>boot.player?playerCSS:options.web?r.webCSS:r.css).replace('<script>/*__BOOT__*/</script>',()=>`<script id="atlas-boot">window.ATLAS_BOOT=${script};</script>`).replace('/*__LIBRARY__*/',()=>r.library).replace('/*__ENGINE__*/',()=>r.engine).replace('/*__APP__*/',()=>boot.player?r.playerApp:r.app);
}
function withRecipe(source,recipe){
 const field=`style: ${recipe.code}`,re=/^---\r?\n([\s\S]*?)\r?\n---/;
 return re.test(source)?source.replace(re,(_,body)=>{
  const rest=body.split(/\r?\n/).filter(l=>!/^\s*(?:layout|theme|style|preset):/.test(l)).join('\n');
  return `---\n${rest?rest+'\n':''}${field}\n---`;
 }):`---\n${field}\n---\n\n${source}`;
}
module.exports={generate,withRecipe};
