/**
 * Online-Course-Creator 使用示例
 * 
 * 运行方式：node example.js
 */

const courseCreator = require('./index.js');

console.log('='.repeat(60));
console.log('🎓 Online-Course-Creator 使用示例');
console.log('='.repeat(60));

// ============================================================================
// 示例 1: 创建完整的 Python 课程
// ============================================================================

console.log('\n📌 示例 1: 创建"Python 数据分析"完整课程\n');

const pythonCourse = courseCreator.createCompleteCourse('Python 数据分析', {
  modules: 8,
  level: 'beginner',
  targetAudience: '零基础学习者',
  includeMarketing: true
});

console.log('\n✅ 课程创建完成!');
console.log(`   主题：${pythonCourse.outline.title}`);
console.log(`   模块数：${pythonCourse.outline.modules.length}`);
console.log(`   预计时长：${pythonCourse.outline.estimatedDuration}`);
console.log(`   视频脚本：${pythonCourse.videoScripts.length}个`);
console.log(`   测验数量：${pythonCourse.quizzes.length}套`);
console.log(`   营销材料：${pythonCourse.marketing ? '包含' : '不包含'}`);

// ============================================================================
// 示例 2: 单独生成课程大纲
// ============================================================================

console.log('\n\n📌 示例 2: 生成"机器学习"课程大纲\n');

const mlOutline = courseCreator.generateCourseOutline('机器学习', 10, 'intermediate');

console.log(`课程：${mlOutline.title}`);
console.log(`副标题：${mlOutline.subtitle}`);
console.log(`难度：${mlOutline.level}`);
console.log(`时长：${mlOutline.estimatedDuration}`);
console.log('\n模块列表:');
mlOutline.modules.forEach(module => {
  console.log(`  ${module.moduleNumber}. ${module.title} - ${module.estimatedTime}`);
});

// ============================================================================
// 示例 3: 生成视频脚本
// ============================================================================

console.log('\n\n📌 示例 3: 生成视频脚本\n');

const videoScript = courseCreator.generateVideoScript(
  'Web 开发',
  'HTML 基础与语义化标签',
  15
);

console.log(`视频标题：${videoScript.metadata.title}`);
console.log(`预计时长：${videoScript.metadata.estimatedDuration}`);
console.log(`目标字数：${videoScript.metadata.targetWordCount}`);
console.log('\n脚本结构:');
console.log(`  • 开场：${videoScript.script.opening.hook.substring(0, 50)}...`);
console.log(`  • 介绍：${videoScript.script.introduction.context.substring(0, 50)}...`);
console.log(`  • 主体内容：${videoScript.script.mainContent.length}个部分`);
console.log(`  • 总结：${videoScript.script.summary.recap.substring(0, 50)}...`);
console.log(`  • 结尾：${videoScript.script.closing.thankYou}`);

// ============================================================================
// 示例 4: 生成测验
// ============================================================================

console.log('\n\n📌 示例 4: 生成"数字营销"测验\n');

const marketingQuiz = courseCreator.generateQuiz('数字营销', 10, 'medium');

console.log(`测验：${marketingQuiz.title}`);
console.log(`难度：${marketingQuiz.difficulty}`);
console.log(`题目数：${marketingQuiz.totalQuestions}`);
console.log(`及格分：${marketingQuiz.passingScore}%`);
console.log(`限时：${marketingQuiz.timeLimit}`);
console.log('\n题目类型分布:');
const typeCount = {};
marketingQuiz.questions.forEach(q => {
  typeCount[q.type] = (typeCount[q.type] || 0) + 1;
});
Object.entries(typeCount).forEach(([type, count]) => {
  console.log(`  • ${type}: ${count}题`);
});

// ============================================================================
// 示例 5: 生成营销材料
// ============================================================================

console.log('\n\n📌 示例 5: 生成"UI 设计"营销材料\n');

const uiMarketing = courseCreator.generateMarketingMaterials('UI 设计', '设计师');

console.log('课程描述 (短版):');
console.log(`  ${uiMarketing.courseDescription.short}`);
console.log('\n落地页标题:');
console.log(`  ${uiMarketing.landingPage.headline}`);
console.log('\n邮件模板 (主题):');
console.log(`  ${uiMarketing.emailTemplates.announcement.subject}`);
console.log('\n微博文案:');
console.log(`  ${uiMarketing.socialMediaPosts.weibo[0]}`);
console.log('\nFAQ 数量:');
console.log(`  ${uiMarketing.faq.length}个问题`);

// ============================================================================
// 示例 6: 导出为 JSON 文件
// ============================================================================

console.log('\n\n📌 示例 6: 导出课程数据\n');

const fs = require('fs');
const path = require('path');

const exportDir = path.join(__dirname, 'exports');
if (!fs.existsSync(exportDir)) {
  fs.mkdirSync(exportDir);
}

const exportFile = path.join(exportDir, 'python-data-analysis-course.json');
fs.writeFileSync(exportFile, JSON.stringify(pythonCourse, null, 2));

console.log(`✅ 课程数据已导出到：${exportFile}`);
console.log(`   文件大小：${(fs.statSync(exportFile).size / 1024).toFixed(2)} KB`);

// ============================================================================
// 完成
// ============================================================================

console.log('\n' + '='.repeat(60));
console.log('✨ 所有示例执行完成!');
console.log('='.repeat(60));
console.log('\n💡 提示:');
console.log('   • 修改 example.js 中的参数来创建不同课程');
console.log('   • 查看 exports 文件夹获取导出的课程数据');
console.log('   • 参考 README.md 了解更多使用方法');
console.log('');
