'use strict';
// Names are stable aliases for presets, never positions in a sorted menu.
const aliases={
 P61:['极简风','清爽','简洁','简单一点','简洁一点','minimalist'],P48:['自然风','读书','书卷','natural'],
 P40:['代码','技术','石板','slate'],P39:['彩虹','演示','rainbow'],
 P60:['暗夜','暗色粉彩','goth pastel'],P65:['手绘','手绘一点','速写','写作草稿','随手画','sketch'],
 P67:['涂鸦','有趣','好玩','有趣一点','好玩一点','脑洞','doodle'],P68:['浮生','小趣','灰驴','小毛驴','生活随想','粉笔夜谈','黑板','粉笔','chalk'],
 P73:['商务','商务一点','正式','正式一点','汇报','business'],P74:['提纲','长文','outline'],
 P75:['组织架构','职责','org chart'],P76:['便签','共创','sticky notes'],
 P77:['概念','分组','concept'],P78:['项目','拆解','任务拆解','project'],
 P79:['索引','复习','index'],P80:['研讨','讨论','workshop']
};
const normalize=value=>String(value).normalize('NFKC').trim().toLowerCase().replace(/[\s·_-]+/g,'');
function catalogue(library){return library.selectedPresets().map(p=>({uid:p.uid,preset:p.id,name:p.name.split(' · ')[0],aliases:aliases[p.id]||[],purpose:p.positioning.useCase,task:p.positioning.task,outcome:p.positioning.outcome,audience:p.positioning.audience,reason:p.description,alternatives:p.positioning.alternatives,code:p.code}));}
function resolve(value,library){
 const text=String(value).trim();
 const preset=library.resolvePreset(text);if(preset)return library.resolveRecipe(preset.id);
 if(/^P\d+$/i.test(text)||/^[A-Z]\d{2}(?:-[A-Z]\d{2}){6}$/i.test(text))return library.resolveRecipe(text);
 const key=normalize(text),found=library.selectedPresets().filter(p=>[p.name,...p.name.split(' · '),...(aliases[p.id]||[])].some(name=>normalize(name)===key));
 if(found.length===1)return library.resolveRecipe(found[0].id);
 if(found.length>1)throw new Error('样式简称有歧义，请使用完整样式名。');
 throw new Error(`没有找到样式“${text}”。可以使用“脑洞涂鸦”“商务”“手绘”“极简”等名称，也可以使用六位 UID（如 MMK0V1），或用 --list 查看16套样式。`);
}
module.exports={catalogue,resolve};
