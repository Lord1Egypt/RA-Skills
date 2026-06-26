/* ====================== 全局固定Header模板 ======================
 * 所有页面统一引用此文件，禁止私自修改Header结构和样式
 * 如需调整Header请统一修改此文件
 * ============================================================= */

document.write(`
<header class="global-header">
    <!-- 左侧Logo -->
    <div class="global-header-left">
        <a href="/" class="logo-container">
            <img src="https://mycntrade.oss-cn-qingdao.aliyuncs.com/zl_platform/file/1774442263059/tanzi_icon01.png" alt="财经探子" class="logo-avatar">
            <span class="logo-text">财经探子</span>
        </a>
    </div>
    <!-- 中间导航菜单（Demo模板占位，后续根据需求替换） -->
    <div class="global-header-center">
        <ul class="global-menu">
            <li><a href="#" class="menu-item active">首页</a></li>
            <li><a href="#" class="menu-item">菜单1</a></li>
            <li><a href="#" class="menu-item">菜单2</a></li>
            <li><a href="#" class="menu-item">菜单3</a></li>
            <li><a href="#" class="menu-item">菜单4</a></li>
        </ul>
    </div>
    <!-- 右侧操作区 -->
    <div class="global-header-right">
        <a href="#" class="upgrade-btn">🚀 升级套餐</a>
    </div>
</header>
`);
