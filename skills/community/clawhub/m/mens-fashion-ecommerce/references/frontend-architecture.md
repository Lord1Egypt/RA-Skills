# 前端架构详细设计

## 项目结构

```
mens-fashion-ecommerce-frontend/
├── public/                      # 静态资源
│   ├── index.html              # 主页面
│   └── favicon.ico             # 网站图标
├── src/                        # 源代码
│   ├── api/                    # API接口
│   │   ├── index.js            # API统一导出
│   │   ├── auth.js             # 认证相关API
│   │   ├── user.js             # 用户相关API
│   │   ├── product.js          # 商品相关API
│   │   ├── cart.js             # 购物车API
│   │   ├── order.js            # 订单API
│   │   └── payment.js          # 支付API
│   ├── assets/                 # 静态资源
│   │   ├── images/             # 图片资源
│   │   ├── styles/             # 样式文件
│   │   └── fonts/              # 字体文件
│   ├── components/             # 公共组件
│   │   ├── common/             # 通用组件
│   │   │   ├── Header.vue      # 头部组件
│   │   │   ├── Footer.vue      # 底部组件
│   │   │   ├── Sidebar.vue     # 侧边栏
│   │   │   └── Breadcrumb.vue  # 面包屑
│   │   ├── layout/             # 布局组件
│   │   └── business/           # 业务组件
│   ├── composables/            # 组合式函数
│   │   ├── useAuth.js          # 认证相关
│   │   ├── useCart.js          # 购物车相关
│   │   └── useProduct.js       # 商品相关
│   ├── router/                 # 路由配置
│   │   ├── index.js            # 路由主文件
│   │   ├── routes.js           # 路由定义
│   │   └── guards.js           # 路由守卫
│   ├── store/                  # 状态管理
│   │   ├── index.js            # Store主文件
│   │   ├── modules/            # 模块化Store
│   │   │   ├── auth.js         # 认证模块
│   │   │   ├── user.js         # 用户模块
│   │   │   ├── product.js      # 商品模块
│   │   │   ├── cart.js         # 购物车模块
│   │   │   └── order.js        # 订单模块
│   │   └── types.js            # 类型定义
│   ├── utils/                  # 工具函数
│   │   ├── request.js          # 请求封装
│   │   ├── auth.js             # 认证工具
│   │   ├── validate.js         # 验证工具
│   │   └── common.js           # 通用工具
│   ├── views/                  # 页面组件
│   │   ├── Home.vue            # 首页
│   │   ├── auth/               # 认证页面
│   │   │   ├── Login.vue       # 登录页
│   │   │   └── Register.vue    # 注册页
│   │   ├── product/            # 商品页面
│   │   │   ├── List.vue        # 商品列表
│   │   │   ├── Detail.vue      # 商品详情
│   │   │   └── Category.vue    # 商品分类
│   │   ├── cart/               # 购物车页面
│   │   │   └── Index.vue       # 购物车主页
│   │   ├── order/              # 订单页面
│   │   │   ├── List.vue        # 订单列表
│   │   │   ├── Detail.vue      # 订单详情
│   │   │   └── Confirm.vue     # 订单确认
│   │   ├── user/               # 用户中心
│   │   │   ├── Profile.vue     # 个人资料
│   │   │   ├── Address.vue     # 地址管理
│   │   │   └── Security.vue    # 安全设置
│   │   └── admin/              # 后台管理
│   │       ├── Dashboard.vue   # 仪表板
│   │       ├── ProductMgr.vue  # 商品管理
│   │       ├── OrderMgr.vue    # 订单管理
│   │       └── UserMgr.vue     # 用户管理
│   ├── App.vue                 # 根组件
│   └── main.js                 # 入口文件
├── .env                        # 环境变量
├── .env.development            # 开发环境变量
├── .env.production             # 生产环境变量
├── vite.config.js              # Vite配置
├── package.json                # 项目配置
└── README.md                   # 项目说明
```

## 核心配置

### 1. Vite配置 (vite.config.js)

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    // 自动导入Element Plus组件
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/assets/styles/variables.scss";`,
      },
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    rollupOptions: {
      output: {
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',
      },
    },
  },
})
```

### 2. 环境变量配置

**.env.development**
```
VITE_APP_TITLE=男装电商系统 - 开发环境
VITE_APP_API_BASE_URL=/api
VITE_APP_UPLOAD_URL=http://localhost:8080/upload
```

**.env.production**
```
VITE_APP_TITLE=男装电商系统
VITE_APP_API_BASE_URL=https://api.mensfashion.com
VITE_APP_UPLOAD_URL=https://api.mensfashion.com/upload
```

### 3. 全局样式 (src/assets/styles/)

**variables.scss** - 样式变量
```scss
// 颜色变量
$primary-color: #409EFF;
$success-color: #67C23A;
$warning-color: #E6A23C;
$danger-color: #F56C6C;
$info-color: #909399;

// 文字颜色
$text-primary: #303133;
$text-regular: #606266;
$text-secondary: #909399;
$text-placeholder: #C0C4CC;

// 边框颜色
$border-base: #DCDFE6;
$border-light: #E4E7ED;
$border-lighter: #EBEEF5;
$border-extra-light: #F2F6FC;

// 背景颜色
$bg-color: #F5F7FA;
$bg-color-light: #F8FAFC;

// 尺寸
$header-height: 60px;
$sidebar-width: 200px;
$footer-height: 60px;

// 响应式断点
$breakpoint-xs: 0;
$breakpoint-sm: 576px;
$breakpoint-md: 768px;
$breakpoint-lg: 992px;
$breakpoint-xl: 1200px;
$breakpoint-xxl: 1400px;
```

**global.scss** - 全局样式
```scss
@import 'variables';

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  font-size: 14px;
  color: $text-primary;
  background-color: $bg-color;
  line-height: 1.5;
}

a {
  color: $primary-color;
  text-decoration: none;
  &:hover {
    color: lighten($primary-color, 10%);
  }
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
}

.page-container {
  min-height: calc(100vh - #{$header-height} - #{$footer-height});
  padding: 20px 0;
}

// 工具类
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.mt-10 { margin-top: 10px; }
.mt-20 { margin-top: 20px; }
.mt-30 { margin-top: 30px; }

.mb-10 { margin-bottom: 10px; }
.mb-20 { margin-bottom: 20px; }
.mb-30 { margin-bottom: 30px; }

.p-10 { padding: 10px; }
.p-20 { padding: 20px; }
.p-30 { padding: 30px; }

.flex { display: flex; }
.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}
.flex-between {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.flex-column { flex-direction: column; }
```

## 核心组件设计

### 1. 请求封装 (src/utils/request.js)

```javascript
import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { useAuthStore } from '@/store/modules/auth'

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_APP_API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json;charset=utf-8',
  },
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers['Authorization'] = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    const res = response.data
    
    // 如果返回的状态码不是200，则判断为错误
    if (res.code !== 200) {
      ElMessage({
        message: res.message || 'Error',
        type: 'error',
        duration: 5 * 1000,
      })
      
      // 401: 未登录
      if (res.code === 401) {
        const authStore = useAuthStore()
        authStore.logout()
        router.push('/login')
      }
      
      // 403: 权限不足
      if (res.code === 403) {
        ElMessage.error('权限不足')
      }
      
      return Promise.reject(new Error(res.message || 'Error'))
    } else {
      return res.data
    }
  },
  (error) => {
    console.log('err' + error)
    
    let message = ''
    if (error.response) {
      switch (error.response.status) {
        case 400:
          message = '请求错误'
          break
        case 401:
          message = '未授权，请重新登录'
          const authStore = useAuthStore()
          authStore.logout()
          router.push('/login')
          break
        case 403:
          message = '拒绝访问'
          break
        case 404:
          message = '请求地址出错'
          break
        case 408:
          message = '请求超时'
          break
        case 500:
          message = '服务器内部错误'
          break
        case 501:
          message = '服务未实现'
          break
        case 502:
          message = '网关错误'
          break
        case 503:
          message = '服务不可用'
          break
        case 504:
          message = '网关超时'
          break
        case 505:
          message = 'HTTP版本不受支持'
          break
        default:
          message = '连接出错'
      }
    } else if (error.message.includes('timeout')) {
      message = '请求超时'
    } else if (error.message.includes('Network Error')) {
      message = '网络错误'
    }
    
    ElMessage({
      message: message || error.message,
      type: 'error',
      duration: 5 * 1000,
    })
    
    return Promise.reject(error)
  }
)

export default service
```

### 2. API接口封装示例 (src/api/auth.js)

```javascript
import request from '@/utils/request'

/**
 * 用户认证API
 */
export const authApi = {
  /**
   * 用户登录
   * @param {Object} data 登录数据
   * @returns {Promise}
   */
  login(data) {
    return request({
      url: '/auth/login',
      method: 'post',
      data,
    })
  },
  
  /**
   * 用户注册
   * @param {Object} data 注册数据
   * @returns {Promise}
   */
  register(data) {
    return request({
      url: '/auth/register',
      method: 'post',
      data,
    })
  },
  
  /**
   * 获取用户信息
   * @returns {Promise}
   */
  getUserInfo() {
    return request({
      url: '/auth/userinfo',
      method: 'get',
    })
  },
  
  /**
   * 退出登录
   * @returns {Promise}
   */
  logout() {
    return request({
      url: '/auth/logout',
      method: 'post',
    })
  },
  
  /**
   * 刷新token
   * @returns {Promise}
   */
  refreshToken() {
    return request({
      url: '/auth/refresh',
      method: 'post',
    })
  },
}
```

### 3. 状态管理 - 认证模块 (src/store/modules/auth.js)

```javascript
import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'
import { getToken, setToken, removeToken } from '@/utils/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: getToken() || '',
    userInfo: null,
    roles: [],
    permissions: [],
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token,
    userName: (state) => state.userInfo?.username || '',
    avatar: (state) => state.userInfo?.avatar || '',
  },
  
  actions: {
    // 用户登录
    async login(loginForm) {
      try {
        const { token } = await authApi.login(loginForm)
        this.token = token
        setToken(token)
        
        // 获取用户信息
        await this.getUserInfo()
        
        return Promise.resolve()
      } catch (error) {
        return Promise.reject(error)
      }
    },
    
    // 获取用户信息
    async getUserInfo() {
      try {
        const userInfo = await authApi.getUserInfo()
        this.userInfo = userInfo
        this.roles = userInfo.roles || []
        this.permissions = userInfo.permissions || []
        
        return Promise.resolve(userInfo)
      } catch (error) {
        return Promise.reject(error)
      }
    },
    
    // 退出登录
    async logout() {
      try {
        await authApi.logout()
      } catch (error) {
        console.error('退出登录失败:', error)
      } finally {
        this.resetToken()
      }
    },
    
    // 重置token
    resetToken() {
      this.token = ''
      this.userInfo = null
      this.roles = []
      this.permissions = []
      removeToken()
    },
    
    // 刷新token
    async refreshToken() {
      try {
        const { token } = await authApi.refreshToken()
        this.token = token
        setToken(token)
        return Promise.resolve(token)
      } catch (error) {
        this.resetToken()
        return Promise.reject(error)
      }
    },
  },
  
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'auth',
        storage: localStorage,
        paths: ['token', 'userInfo'],
      },
    ],
  },
})
```

### 4. 路由配置 (src/router/index.js)

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes'
import { useAuthStore } from '@/store/modules/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  },
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore