"use strict";
/**
 * Memory-Master v4.0
 *
 * 基于 Karpathy 方法论 + Anthropic 官方经验 + Claude Code 架构
 * 整合 30 篇行业最佳实践笔记
 *
 * @author 小鬼 👻 + Jake
 * @version 4.0.0
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateOptimizationReport = exports.runFilterTests = exports.detectSensitiveData = exports.filterSensitiveData = exports.SkillsBenchBenchmark = exports.SkillCraftBenchmark = exports.PerformanceMonitor = exports.SkillEvolver = exports.TokenOptimizer = exports.MemoryCompactor = exports.MemoryRetriever = exports.MemoryCapture = exports.MemoryMaster = void 0;
const capture_1 = require("./capture");
Object.defineProperty(exports, "MemoryCapture", { enumerable: true, get: function () { return capture_1.MemoryCapture; } });
const retrieve_1 = require("./retrieve");
Object.defineProperty(exports, "MemoryRetriever", { enumerable: true, get: function () { return retrieve_1.MemoryRetriever; } });
const compact_1 = require("./compact");
Object.defineProperty(exports, "MemoryCompactor", { enumerable: true, get: function () { return compact_1.MemoryCompactor; } });
const filter_1 = require("./filter");
Object.defineProperty(exports, "filterSensitiveData", { enumerable: true, get: function () { return filter_1.filterSensitiveData; } });
Object.defineProperty(exports, "detectSensitiveData", { enumerable: true, get: function () { return filter_1.detectSensitiveData; } });
Object.defineProperty(exports, "runFilterTests", { enumerable: true, get: function () { return filter_1.runFilterTests; } });
const token_optimizer_1 = require("./token-optimizer");
Object.defineProperty(exports, "TokenOptimizer", { enumerable: true, get: function () { return token_optimizer_1.TokenOptimizer; } });
Object.defineProperty(exports, "generateOptimizationReport", { enumerable: true, get: function () { return token_optimizer_1.generateOptimizationReport; } });
const skill_evolver_1 = require("./skill-evolver");
Object.defineProperty(exports, "SkillEvolver", { enumerable: true, get: function () { return skill_evolver_1.SkillEvolver; } });
const benchmark_1 = require("./benchmark");
Object.defineProperty(exports, "PerformanceMonitor", { enumerable: true, get: function () { return benchmark_1.PerformanceMonitor; } });
Object.defineProperty(exports, "SkillCraftBenchmark", { enumerable: true, get: function () { return benchmark_1.SkillCraftBenchmark; } });
Object.defineProperty(exports, "SkillsBenchBenchmark", { enumerable: true, get: function () { return benchmark_1.SkillsBenchBenchmark; } });
/**
 * Memory-Master 主类
 */
class MemoryMaster {
    constructor(memoryDir = 'memory') {
        this.captureModule = new capture_1.MemoryCapture(memoryDir);
        this.retrieveModule = new retrieve_1.MemoryRetriever(memoryDir);
        this.compactor = new compact_1.MemoryCompactor(memoryDir);
        this.tokenOptimizer = new token_optimizer_1.TokenOptimizer(memoryDir);
        this.skillEvolver = new skill_evolver_1.SkillEvolver(memoryDir);
        this.monitor = new benchmark_1.PerformanceMonitor(memoryDir);
        this.skillCraftBenchmark = new benchmark_1.SkillCraftBenchmark(memoryDir);
        this.skillsBenchBenchmark = new benchmark_1.SkillsBenchBenchmark(memoryDir);
    }
    /**
     * 捕捉记忆
     */
    async capture(content, options) {
        const startTime = Date.now();
        const result = await this.captureModule.capture(content, options);
        // 记录性能
        this.monitor.recordResponseTime(Date.now() - startTime);
        return result;
    }
    /**
     * 检索记忆
     */
    async retrieve(query, options) {
        const startTime = Date.now();
        const result = await this.retrieveModule.retrieve(query, options);
        // 记录性能
        this.monitor.recordResponseTime(Date.now() - startTime);
        return result;
    }
    /**
     * 压缩记忆
     */
    async compact(options) {
        return this.compactor.compact(options);
    }
    /**
     * 过滤敏感数据
     */
    async filter(content) {
        return (0, filter_1.filterSensitiveData)(content);
    }
    /**
     * 检测敏感数据
     */
    async detect(content) {
        return (0, filter_1.detectSensitiveData)(content);
    }
    /**
     * Token 优化
     */
    async optimizeTokens() {
        // TODO: 实现记忆加载
        const memories = []; // 待实现
        return (0, token_optimizer_1.generateOptimizationReport)(memories, this.tokenOptimizer);
    }
    /**
     * 记录经验
     */
    async recordExperience(context, action, result, feedback) {
        return this.skillEvolver.recordExperience(context, action, result, feedback);
    }
    /**
     * 技能蒸馏
     */
    async distillSkills() {
        return this.skillEvolver.distillSkills();
    }
    /**
     * 获取评测报告
     */
    async getBenchmarkReport(name) {
        return this.monitor.generateBenchmarkReport(name);
    }
    /**
     * 运行 SkillCraft 评测
     */
    async runSkillCraftBenchmark(tasks) {
        return this.skillCraftBenchmark.evaluateToolUsage(tasks);
    }
    /**
     * 运行 SkillsBench 评测
     */
    async runSkillsBenchBenchmark(tasks) {
        return this.skillsBenchBenchmark.evaluateAcrossTasks(tasks);
    }
    /**
     * 运行测试
     */
    async test() {
        console.log('🧪 Memory-Master v4.0 测试');
        console.log('=========================\n');
        // 运行过滤测试
        await (0, filter_1.runFilterTests)();
        console.log('\n✅ 所有测试完成！');
    }
}
exports.MemoryMaster = MemoryMaster;
exports.default = MemoryMaster;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaW5kZXguanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9zcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IjtBQUFBOzs7Ozs7OztHQVFHOzs7QUFFSCx1Q0FBeUU7QUFrSnZFLDhGQWxKTyx1QkFBYSxPQWtKUDtBQWpKZix5Q0FBc0Y7QUFrSnBGLGdHQWxKTywwQkFBZSxPQWtKUDtBQWpKakIsdUNBQTJFO0FBa0p6RSxnR0FsSk8seUJBQWUsT0FrSlA7QUFqSmpCLHFDQUFvRjtBQXFLbEYsb0dBcktPLDRCQUFtQixPQXFLUDtBQUNuQixvR0F0SzRCLDRCQUFtQixPQXNLNUI7QUFDbkIsK0ZBdktpRCx1QkFBYyxPQXVLakQ7QUF0S2hCLHVEQUEySDtBQWlKekgsK0ZBakpPLGdDQUFjLE9BaUpQO0FBc0JkLDJHQXZLZ0QsNENBQTBCLE9BdUtoRDtBQXRLNUIsbURBQStDO0FBaUo3Qyw2RkFqSk8sNEJBQVksT0FpSlA7QUFoSmQsMkNBQTRGO0FBaUoxRixtR0FqSk8sOEJBQWtCLE9BaUpQO0FBQ2xCLG9HQWxKMkIsK0JBQW1CLE9Ba0ozQjtBQUNuQixxR0FuSmdELGdDQUFvQixPQW1KaEQ7QUFqSnRCOztHQUVHO0FBQ0gsTUFBYSxZQUFZO0lBVXZCLFlBQVksWUFBb0IsUUFBUTtRQUN0QyxJQUFJLENBQUMsYUFBYSxHQUFHLElBQUksdUJBQWEsQ0FBQyxTQUFTLENBQUMsQ0FBQztRQUNsRCxJQUFJLENBQUMsY0FBYyxHQUFHLElBQUksMEJBQWUsQ0FBQyxTQUFTLENBQUMsQ0FBQztRQUNyRCxJQUFJLENBQUMsU0FBUyxHQUFHLElBQUkseUJBQWUsQ0FBQyxTQUFTLENBQUMsQ0FBQztRQUNoRCxJQUFJLENBQUMsY0FBYyxHQUFHLElBQUksZ0NBQWMsQ0FBQyxTQUFTLENBQUMsQ0FBQztRQUNwRCxJQUFJLENBQUMsWUFBWSxHQUFHLElBQUksNEJBQVksQ0FBQyxTQUFTLENBQUMsQ0FBQztRQUNoRCxJQUFJLENBQUMsT0FBTyxHQUFHLElB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QUMsQ0FBQztJQUM5RCxDQUFDO0lBRUQ7O09BRUc7SUFDSCxLQUFLLENBQUMsSUFBSTtRQUNSLE9BQU8sQ0FBQyxHQUFHLENBQUMsMEJBQTBCLENBQUMsQ0FBQztRQUN4QyxPQUFPLENBQUMsR0FBRyxDQUFDLDZCQUE2QixDQUFDLENBQUM7UUFFM0MsU0FBUztRQUNULE1BQU0sSUFBQSx1QkFBYyxHQUFFLENBQUM7UUFFdkIsT0FBTyxDQUFDLEdBQUcsQ0FBQyxhQUFhLENBQUMsQ0FBQztJQUM3QixDQUFDO0NBQ0Y7QUFqSUQsb0NBaUlDO0FBa0NELGtCQUFlLFlBQVksQ0FBQyIsInNvdXJjZXNDb250ZW50IjpbIi8qKlxuICogTWVtb3J5LU1hc3RlciB2NC4wXG4gKiBcbiAqIOWfuuS6jiBLYXJwYXRoeSDmlrnms5XorrogKyBBbnRocm9waWMg5a6Y5pa557uP6aqMICsgQ2xhdWRlIENvZGUg5p625p6EXG4gKiDmlbTlkIggMzAg56+H6KGM5Lia5pyA5L2z5a6e6Le156yU6K6wXG4gKiBcbiAqIEBhdXRob3Ig5bCP6ay8IPCfkbsgKyBKYWtlXG4gKiBAdmVyc2lvbiA0LjAuMFxuICovXG5cbmltcG9ydCB7IE1lbW9yeUNhcHR1cmUsIENhcHR1cmVPcHRpb25zLCBDYXB0dXJlUmVzdWx0IH0gZnJvbSAnLi9jYXB0dXJlJztcbmltcG9ydCB7IE1lbW9yeVJldHJpZXZlciwgUmV0cmlldmVPcHRpb25zLCBSZXRyaWV2ZVJlc3VsdCwgTWVtb3J5IH0gZnJvbSAnLi9yZXRyaWV2ZSc7XG5pbXBvcnQgeyBNZW1vcnlDb21wYWN0b3IsIENvbXBhY3RPcHRpb25zLCBDb21wYWN0UmVzdWx0IH0gZnJvbSAnLi9jb21wYWN0JztcbmltcG9ydCB7IGZpbHRlclNlbnNpdGl2ZURhdGEsIGRldGVjdFNlbnNpdGl2ZURhdGEsIHJ1bkZpbHRlclRlc3RzIH0gZnJvbSAnLi9maWx0ZXInO1xuaW1wb3J0IHsgVG9rZW5PcHRpbWl6ZXIsIFRva2VuT3B0aW1pemF0aW9uUmVwb3J0LCBnZW5lcmF0ZU9wdGltaXphdGlvblJlcG9ydCwgUHJpb3JpdGl6ZWRNZW1vcnkgfSBmcm9tICcuL3Rva2VuLW9wdGltaXplcic7XG5pbXBvcnQgeyBTa2lsbEV2b2x2ZXIgfSBmcm9tICcuL3NraWxsLWV2b2x2ZXInO1xuaW1wb3J0IHsgUGVyZm9ybWFuY2VNb25pdG9yLCBTa2lsbENyYWZ0QmVuY2htYXJrLCBTa2lsbHNCZW5jaEJlbmNobWFyayB9IGZyb20gJy4vYmVuY2htYXJrJztcblxuLyoqXG4gKiBNZW1vcnktTWFzdGVyIOS4u+exu1xuICovXG5leHBvcnQgY2xhc3MgTWVtb3J5TWFzdGVyIHtcbiAgcHJpdmF0ZSBjYXB0dXJlTW9kdWxlOiBNZW1vcnlDYXB0dXJlO1xuICBwcml2YXRlIHJldHJpZXZlTW9kdWxlOiBNZW1vcnlSZXRyaWV2ZXI7XG4gIHByaXZhdGUgY29tcGFjdG9yOiBNZW1vcnlDb21wYWN0b3I7XG4gIHByaXZhdGUgdG9rZW5PcHRpbWl6ZXI6IFRva2VuT3B0aW1pemVyO1xuICBwcml2YXRlIHNraWxsRXZvbHZlcjogU2tpbGxFdm9sdmVyO1xuICBwcml2YXRlIG1vbml0b3I6IFBlcmZvcm1hbmNlTW9uaXRvcjtcbiAgcHJpdmF0ZSBza2lsbENyYWZ0QmVuY2htYXJrOiBTa2lsbENyYWZ0QmVuY2htYXJrO1xuICBwcml2YXRlIHNraWxsc0JlbmNoQmVuY2htYXJrOiBTa2lsbHNCZW5jaEJlbmNobWFyaztcblxuICBjb25zdHJ1Y3RvcihtZW1vcnlEaXI6IHN0cmluZyA9ICdtZW1vcnknKSB7XG4gICAgdGhpcy5jYXB0dXJlTW9kdWxlID0gbmV3IE1lbW9yeUNhcHR1cmUobWVtb3J5RGlyKTtcbiAgICB0aGlzLnJldHJpZXZlTW9kdWxlID0gbmV3IE1lbW9yeVJldHJpZXZlcihtZW1vcnlEaXIpO1xuICAgIHRoaXMuY29tcGFjdG9yID0gbmV3IE1lbW9yeUNvbXBhY3RvcihtZW1vcnlEaXIpO1xuICAgIHRoaXMudG9rZW5PcHRpbWl6ZXIgPSBuZXcgVG9rZW5PcHRpbWl6ZXIobWVtb3J5RGlyKTtcbiAgICB0aGlzLnNraWxsRXZvbHZlciA9IG5ldyBTa2lsbEV2b2x2ZXIobWVtb3J5RGlyKTtcbiAgICB0aGlzLm1vbml0b3IgPSBuZXcgUGVyZm9ybWFuY2VNb25pdG9yKG1lbW9yeURpcik7XG4gICAgdGhpcy5za2lsbENyYWZ0QmVuY2htYXJrID0gbmV3IFNraWxsQ3JhZnRCZW5jaG1hcmsobWVtb3J5RGlyKTtcbiAgICB0aGlzLnNraWxsc0JlbmNoQmVuY2htYXJrID0gbmV3IFNraWxsc0JlbmNoQmVuY2htYXJrKG1lbW9yeURpcik7XG4gIH1cblxuICAvKipcbiAgICog5o2V5o2J6K6w5b+GXG4gICAqL1xuICBhc3luYyBjYXB0dXJlKGNvbnRlbnQ6IHN0cmluZywgb3B0aW9ucz86IENhcHR1cmVPcHRpb25zKTogUHJvbWlzZTxDYXB0dXJlUmVzdWx0PiB7XG4gICAgY29uc3Qgc3RhcnRUaW1lID0gRGF0ZS5ub3coKTtcbiAgICBjb25zdCByZXN1bHQgPSBhd2FpdCB0aGlzLmNhcHR1cmVNb2R1bGUuY2FwdHVyZShjb250ZW50LCBvcHRpb25zKTtcbiAgICBcbiAgICAvLyDorrDlvZXmgKfog71cbiAgICB0aGlzLm1vbml0b3IucmVjb3JkUmVzcG9uc2VUaW1lKERhdGUubm93KCkgLSBzdGFydFRpbWUpO1xuICAgIFxuICAgIHJldHVybiByZXN1bHQ7XG4gIH1cblxuICAvKipcbiAgICog5qOA57Si6K6w5b+GXG4gICAqL1xuICBhc3luYyByZXRyaWV2ZShxdWVyeTogc3RyaW5nLCBvcHRpb25zPzogUmV0cmlldmVPcHRpb25zKTogUHJvbWlzZTxSZXRyaWV2ZVJlc3VsdD4ge1xuICAgIGNvbnN0IHN0YXJ0VGltZSA9IERhdGUubm93KCk7XG4gICAgY29uc3QgcmVzdWx0ID0gYXdhaXQgdGhpcy5yZXRyaWV2ZU1vZHVsZS5yZXRyaWV2ZShxdWVyeSwgb3B0aW9ucyk7XG4gICAgXG4gICAgLy8g6K6w5b2V5oCn6IO9XG4gICAgdGhpcy5tb25pdG9yLnJlY29yZFJlc3BvbnNlVGltZShEYXRlLm5vdygpIC0gc3RhcnRUaW1lKTtcbiAgICBcbiAgICByZXR1cm4gcmVzdWx0O1xuICB9XG5cbiAgLyoqXG4gICAqIOWOi+e8qeiusOW/hlxuICAgKi9cbiAgYXN5bmMgY29tcGFjdChvcHRpb25zPzogQ29tcGFjdE9wdGlvbnMpOiBQcm9taXNlPENvbXBhY3RSZXN1bHQ+IHtcbiAgICByZXR1cm4gdGhpcy5jb21wYWN0b3IuY29tcGFjdChvcHRpb25zKTtcbiAgfVxuXG4gIC8qKlxuICAgKiDov4fmu6TmlY/mhJ/mlbDmja5cbiAgICovXG4gIGFzeW5jIGZpbHRlcihjb250ZW50OiBzdHJpbmcpIHtcbiAgICByZXR1cm4gZmlsdGVyU2Vuc2l0aXZlRGF0YShjb250ZW50KTtcbiAgfVxuXG4gIC8qKlxuICAgKiDmo4DmtYvmlY/mhJ/mlbDmja5cbiAgICovXG4gIGFzeW5jIGRldGVjdChjb250ZW50OiBzdHJpbmcpIHtcbiAgICByZXR1cm4gZGV0ZWN0U2Vuc2l0aXZlRGF0YShjb250ZW50KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUb2tlbiDkvJjljJZcbiAgICovXG4gIGFzeW5jIG9wdGltaXplVG9rZW5zKCk6IFByb21pc2U8VG9rZW5PcHRpbWl6YXRpb25SZXBvcnQ+IHtcbiAgICAvLyBUT0RPOiDlrp7njrDorrDlv4bliqDovb1cbiAgICBjb25zdCBtZW1vcmllczogUHJpb3JpdGl6ZWRNZW1vcnlbXSA9IFtdOyAvLyDlvoXlrp7njrBcbiAgICByZXR1cm4gZ2VuZXJhdGVPcHRpbWl6YXRpb25SZXBvcnQobWVtb3JpZXMsIHRoaXMudG9rZW5PcHRpbWl6ZXIpO1xuICB9XG5cbiAgLyoqXG4gICAqIOiusOW9lee7j+mqjFxuICAgKi9cbiAgYXN5bmMgcmVjb3JkRXhwZXJpZW5jZShcbiAgICBjb250ZXh0OiBzdHJpbmcsXG4gICAgYWN0aW9uOiBzdHJpbmcsXG4gICAgcmVzdWx0OiAnc3VjY2VzcycgfCAnZmFpbHVyZScsXG4gICAgZmVlZGJhY2s/OiBzdHJpbmdcbiAgKSB7XG4gICAgcmV0dXJuIHRoaXMuc2tpbGxFdm9sdmVyLnJlY29yZEV4cGVyaWVuY2UoY29udGV4dCwgYWN0aW9uLCByZXN1bHQsIGZlZWRiYWNrKTtcbiAgfVxuXG4gIC8qKlxuICAgKiDmioDog73okrjppo9cbiAgICovXG4gIGFzeW5jIGRpc3RpbGxTa2lsbHMoKSB7XG4gICAgcmV0dXJuIHRoaXMuc2tpbGxFdm9sdmVyLmRpc3RpbGxTa2lsbHMoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiDojrflj5bor4TmtYvmiqXlkYpcbiAgICovXG4gIGFzeW5jIGdldEJlbmNobWFya1JlcG9ydChuYW1lPzogc3RyaW5nKSB7XG4gICAgcmV0dXJuIHRoaXMubW9uaXRvci5nZW5lcmF0ZUJlbmNobWFya1JlcG9ydChuYW1lKTtcbiAgfVxuXG4gIC8qKlxuICAgKiDov5DooYwgU2tpbGxDcmFmdCDor4TmtYtcbiAgICovXG4gIGFzeW5jIHJ1blNraWxsQ3JhZnRCZW5jaG1hcmsodGFza3M6IGFueVtdKSB7XG4gICAgcmV0dXJuIHRoaXMuc2tpbGxDcmFmdEJlbmNobWFyay5ldmFsdWF0ZVRvb2xVc2FnZSh0YXNrcyk7XG4gIH1cblxuICAvKipcbiAgICog6L+Q6KGMIFNraWxsc0JlbmNoIOivhOa1i1xuICAgKi9cbiAgYXN5bmMgcnVuU2tpbGxzQmVuY2hCZW5jaG1hcmsodGFza3M6IGFueVtdKSB7XG4gICAgcmV0dXJuIHRoaXMuc2tpbGxzQmVuY2hCZW5jaG1hcmsuZXZhbHVhdGVBY3Jvc3NUYXNrcyh0YXNrcyk7XG4gIH1cblxuICAvKipcbiAgICog6L+Q6KGM5rWL6K+VXG4gICAqL1xuICBhc3luYyB0ZXN0KCk6IFByb21pc2U8dm9pZD4ge1xuICAgIGNvbnNvbGUubG9nKCfwn6eqIE1lbW9yeS1NYXN0ZXIgdjQuMCDmtYvor5UnKTtcbiAgICBjb25zb2xlLmxvZygnPT09PT09PT09PT09PT09PT09PT09PT09PVxcbicpO1xuICAgIFxuICAgIC8vIOi/kOihjOi/h+a7pOa1i+ivlVxuICAgIGF3YWl0IHJ1bkZpbHRlclRlc3RzKCk7XG4gICAgXG4gICAgY29uc29sZS5sb2coJ1xcbuKchSDmiYDmnInmtYvor5XlrozmiJDvvIEnKTtcbiAgfVxufVxuXG4vKipcbiAqIOWvvOWHuuexu+Wei1xuICovXG5leHBvcnQge1xuICBNZW1vcnlDYXB0dXJlLFxuICBNZW1vcnlSZXRyaWV2ZXIsXG4gIE1lbW9yeUNvbXBhY3RvcixcbiAgVG9rZW5PcHRpbWl6ZXIsXG4gIFNraWxsRXZvbHZlcixcbiAgUGVyZm9ybWFuY2VNb25pdG9yLFxuICBTa2lsbENyYWZ0QmVuY2htYXJrLFxuICBTa2lsbHNCZW5jaEJlbmNobWFyayxcbiAgQ2FwdHVyZU9wdGlvbnMsXG4gIENhcHR1cmVSZXN1bHQsXG4gIFJldHJpZXZlT3B0aW9ucyxcbiAgUmV0cmlldmVSZXN1bHQsXG4gIENvbXBhY3RPcHRpb25zLFxuICBDb21wYWN0UmVzdWx0LFxuICBUb2tlbk9wdGltaXphdGlvblJlcG9ydCxcbiAgTWVtb3J5LFxufTtcblxuLyoqXG4gKiDlr7zlh7rlt6Xlhbflh73mlbBcbiAqL1xuZXhwb3J0IHtcbiAgZmlsdGVyU2Vuc2l0aXZlRGF0YSxcbiAgZGV0ZWN0U2Vuc2l0aXZlRGF0YSxcbiAgcnVuRmlsdGVyVGVzdHMsXG4gIGdlbmVyYXRlT3B0aW1pemF0aW9uUmVwb3J0LFxufTtcblxuZXhwb3J0IGRlZmF1bHQgTWVtb3J5TWFzdGVyO1xuIl19