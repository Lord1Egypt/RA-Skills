#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const runtime=path.join(__dirname,'../assets/runtime'),K=require(path.join(runtime,'src/engine.cjs')),L=K.library,D=require(path.join(runtime,'src/document.cjs'));
const Names=require('./style-names.cjs');
function readSource(input){
 if(input==='-')return {source:fs.readFileSync(0,'utf8').replace(/^\uFEFF/,'')};
 const source=fs.readFileSync(input,'utf8').replace(/^\uFEFF/,'');if(!/\.html?$/i.test(input))return {source};
 const script=source.match(/<script\b[^>]*\sid=(["'])atlas-boot\1[^>]*>([\s\S]*?)<\/script\s*>/i),boot=script?.[2].match(/^\s*window\.ATLAS_BOOT\s*=\s*([\s\S]*?)\s*;?\s*$/);
 if(!boot)throw new Error('这个HTML没有Mindbox的可编辑内容，请提供配套Markdown。');
 let data;try{data=JSON.parse(boot[1]);}catch{throw new Error('HTML中的Mindbox数据无法读取，请提供配套Markdown。');}
 if(typeof data?.source!=='string')throw new Error('HTML缺少可编辑内容，请提供配套Markdown。');
 const options=K.parseOptions(data.source);let recipe=L.resolveRecipe(data.recipeCode||data.preset||(data.theme?L.legacy[data.theme]:options.recipeCode||'P61'));
 if(data.layout)recipe=L.replaceToken(recipe,'L',L.axes.L.items.find(l=>l.id===data.layout)?.code);
 const model=require(path.join(runtime,'src/edit.cjs')).create(data);
 return {source:data.document?model.markdown(recipe.code):D.withRecipe(data.source,recipe),recipeCode:recipe.code,document:data.document?model.document():null,view:data.view,selectedRecipeCode:data.selectedRecipeCode,editorView:data.editorView,...(data.markdownDraft!==undefined?{markdownDraft:data.markdownDraft}:{})};
}
function verifyRuntime(){
 try{
  const manifest=JSON.parse(fs.readFileSync(path.join(runtime,'manifest.json'),'utf8'));
  if(manifest.format!==1||!manifest.files||!Object.keys(manifest.files).length)throw new Error('缺少有效清单');
  for(const [name,expected] of Object.entries(manifest.files)){
   const file=path.resolve(runtime,name);if(!file.startsWith(runtime+path.sep))throw new Error('资源路径无效');
   if(crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')!==expected)throw new Error(name+' 与打包版本不一致');
  }
  const digest=crypto.createHash('sha256').update(JSON.stringify(manifest.files)).digest('hex');
  if(digest!==manifest.renderer)throw new Error('清单指纹不一致');return digest;
 }catch(error){throw new Error('模板资源校验失败：'+error.message+'。请重新打包或更新 Skill，不要另写一套页面。');}
}
function validateDocument(html,source,recipe){
 const script=html.match(/<script id="atlas-boot">window\.ATLAS_BOOT=([\s\S]*?);<\/script>/);
 const boot=script&&JSON.parse(script[1]);
 if(!boot||boot.source!==source||boot.recipeCode!==recipe.code||!boot.player||!boot.standalone)throw new Error('模板内容或配方注入校验失败');
 if(!html.includes('data:font/woff2;base64,')||/<script[^>]+src=|<link[^>]+(?:stylesheet|preload)/.test(html)||/url\((?:https?:|fonts\/)/.test(html))throw new Error('模板离线资源校验失败');
}
function main(args){
 const opts={};for(let i=0;i<args.length;i++){const key=args[i];if(['--list','--compact','--force','--help','--extract','--check','--version'].includes(key))opts[key]=true;else if(['--input','--output','--preset','--style','--switch-to','--revise'].includes(key)){if(!args[i+1]||args[i+1].startsWith('--'))throw new Error('缺少参数：'+key);opts[key]=args[++i];}else throw new Error('未知参数：'+key);}
 if(opts['--version']){console.log(require('../version.json').version);return;}
 if(opts['--help']){console.log('生成：node render.cjs --input draft.md --output map.html --preset "MMP0A7"（也可用“脑洞涂鸦”）\n切换：node render.cjs --input map.md --switch-to "商务"\n也支持MindboxHTML作为输入；切换默认另存为 map--MMC0Y9.html 与 .md，保留原文件。\n--input - 从标准输入提交Markdown（须指定--output）；--list --compact 查看轻量目录；--input map.html --extract 读取 HTML 最新内容到标准输出。\n--input map.html --revise - 从标准输入修订同一个 HTML；--style 指定七维组合；--force 明确覆盖已有输出；--input map.html --check 独立复查最终 HTML 与内容哈希。');return;}
 if(opts['--list']){const list=Names.catalogue(L);console.log(JSON.stringify(opts['--compact']?list.map(({uid,preset,name,purpose})=>({uid,preset,name,purpose})):list,null,opts['--compact']?0:2));return;}
 if(opts['--check']){if(!opts['--input']||opts['--input']==='-'||Object.keys(opts).some(k=>!['--input','--check'].includes(k)))throw new Error('--check 仅与 --input map.html 搭配。');verifyRuntime();console.log(JSON.stringify({checkerVersion:require('../version.json').version,...require('./check.cjs').inspectHTML(fs.readFileSync(path.resolve(opts['--input']),'utf8'))},null,2));return;}
 if(opts['--extract']){if(!opts['--input']||opts['--output']||opts['--switch-to']||opts['--preset']||opts['--style']||opts['--force']||opts['--revise'])throw new Error('--extract 仅与 --input 搭配。');verifyRuntime();const current=readSource(opts['--input']==='-'?'-':path.resolve(opts['--input']));process.stdout.write(current.markdownDraft??current.source);return;}
 if(!opts['--input']||(!opts['--output']&&!opts['--switch-to']&&!opts['--revise']))throw new Error('请提供 --input 与 --output；换风格可改用 --input 与 --switch-to。');
 if(['--preset','--style','--switch-to'].filter(k=>opts[k]).length>1)throw new Error('--preset、--style 与 --switch-to 只选一个。');
 if(opts['--input']==='-'&&!opts['--output'])throw new Error('标准输入需要指定 --output HTML路径。');
 if(opts['--revise']&&(!/\.html?$/i.test(opts['--input'])||opts['--input']==='-'))throw new Error('--revise 需要现有 HTML 作为 --input。');
 const renderer=verifyRuntime(),input=opts['--input']==='-'?'-':path.resolve(opts['--input']),inputData=readSource(input);
 if(opts['--revise']){Object.assign(inputData,require(path.join(runtime,'src/edit.cjs')).revise(inputData,readSource(opts['--revise']==='-'?'-':path.resolve(opts['--revise'])).source));delete inputData.markdownDraft;inputData.editorView='map';}
 const source=inputData.source,tree=K.parseMindmap(source),options=K.parseOptions(source);
 const selected=opts['--switch-to']||opts['--style']||opts['--preset']||options.recipeCode||(options.theme?L.legacy[options.theme]:inputData.recipeCode||'P61');
 let recipe=Names.resolve(selected,L);if(!opts['--style']&&!opts['--preset']&&!opts['--switch-to']&&options.layout)recipe=L.replaceToken(recipe,'L',L.axes.L.items.find(l=>l.id===options.layout).code);
 const stem=path.basename(input,path.extname(input)).replace(/--(?:P\d+|MM[A-Z0-9]{4}|custom)(?:-\d+)?$/i,'');
 let output=opts['--output']?path.resolve(opts['--output']):opts['--revise']?input:path.join(path.dirname(input),`${stem}--${recipe.preset?.uid||recipe.preset?.id||'custom'}.html`);
 if(!opts['--output']&&!opts['--force']&&!opts['--revise']){const base=output.slice(0,-5);let version=2;while(fs.existsSync(output)||fs.existsSync(output.slice(0,-5)+'.md'))output=`${base}-${version++}.html`;}
 if(path.extname(output).toLowerCase()!=='.html')throw new Error('输出文件请使用 .html 后缀。');
 const md=output.slice(0,-5)+'.md',inPlace=Boolean(opts['--revise'])&&output===input;
 for(const file of [output,md])if(fs.existsSync(file)&&!opts['--force']&&!inPlace)throw new Error('文件已存在：'+file+'。确认需要更新时使用 --force。');
 const normalized=D.withRecipe(source,recipe);
 const html=D.generate({source:normalized,recipeCode:recipe.code,standalone:true,player:true,...(inputData.document?{document:inputData.document,view:inputData.view}:{}),...(inputData.editorView?{editorView:inputData.editorView}:{}),...(inputData.markdownDraft!==undefined?{markdownDraft:inputData.markdownDraft}:{}),...(!opts['--switch-to']&&!opts['--preset']&&!opts['--style']&&inputData.selectedRecipeCode?{selectedRecipeCode:inputData.selectedRecipeCode}:{})});validateDocument(html,normalized,recipe);require('./check.cjs').inspectHTML(html);
 fs.mkdirSync(path.dirname(output),{recursive:true});
 require('./deliver.cjs').deliver([[md,normalized],[output,html]],{force:Boolean(opts['--force'])||inPlace});
 const checked=require('./check.cjs').inspectHTML(fs.readFileSync(output,'utf8'));
 const levels=n=>1+Math.max(0,...n.children.map(levels));
 console.log(JSON.stringify({version:require('../version.json').version,html:output,markdown:md,uid:recipe.preset?.uid||null,preset:recipe.preset?.id||null,name:recipe.preset?.name.split(' · ')[0]||'自定义',style:recipe.code,nodes:K.descendants(tree)+1,restyled:Boolean(opts['--switch-to']),revised:Boolean(opts['--revise']),renderer,pendingMarkdown:checked.pendingMarkdown,sha256:checked.sha256,validation:{passed:true,kind:'structural',browserChecked:false,levels:levels(tree),standalone:true}},null,2));
}
try{main(process.argv.slice(2));}catch(error){console.error(error.message);process.exitCode=1;}
