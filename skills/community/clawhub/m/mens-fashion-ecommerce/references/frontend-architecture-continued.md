// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // 设置页面标题
  const title = to.meta?.title || '男装电商系统'
  document.title = `${title} - ${import.meta.env.VITE_APP_TITLE}`
  
  // 检查是否需要认证
  if (to.meta?.requiresAuth) {
    if (authStore.isLoggedIn) {
      // 检查用户角色权限
      if (to.meta?.roles && to.meta.roles.length > 0) {
        const hasRole = authStore.roles.some(role => to.meta.roles.includes(role))
        if (!hasRole) {
          next('/403')
          return
        }
      }
      next()
    } else {
      next({
        path: '/login',
        query: { redirect: to.fullPath },
      })
    }
  } else {
    next()
  }
})

export default router

### 5. 路由定义 (src/router/routes.js)

```javascript
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: {
      title: '首页',
      requiresAuth: false,
    },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: {
      title: '登录',
      requiresAuth: false,
    },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: {
      title: '注册',
      requiresAuth: false,
    },
  },
  {
    path: '/products',
    name: 'ProductList',
    component: () => import('@/views/product/List.vue'),
    meta: {
      title: '商品列表',
      requiresAuth: false,
    },
  },
  {
    path: '/products/:id',
    name: 'ProductDetail',
    component: () => import('@/views/product/Detail.vue'),
    meta: {
      title: '商品详情',
      requiresAuth: false,
    },
  },
  {
    path: '/cart',
    name: 'Cart',
    component: () => import('@/views/cart/Index.vue'),
    meta: {
      title: '购物车',
      requiresAuth: true,
    },
  },
  {
    path: '/order/confirm',
    name: 'OrderConfirm',
    component: () => import('@/views/order/Confirm.vue'),
    meta: {
      title: '订单确认',
      requiresAuth: true,
    },
  },
  {
    path: '/orders',
    name: 'OrderList',
    component: () => import('@/views/order/List.vue'),
    meta: {
      title: '我的订单',
      requiresAuth: true,
    },
  },
  {
    path: '/orders/:id',
    name: 'OrderDetail',
    component: () => import('@/views/order/Detail.vue'),
    meta: {
      title: '订单详情',
      requiresAuth: true,
    },
  },
  {
    path: '/user/profile',
    name: 'UserProfile',
    component: () => import('@/views/user/Profile.vue'),
    meta: {
      title: '个人资料',
      requiresAuth: true,
    },
  },
  {
    path: '/user/address',
    name: 'UserAddress',
    component: () => import('@/views/user/Address.vue'),
    meta: {
      title: '地址管理',
      requiresAuth: true,
    },
  },
  // 后台管理路由
  {
    path: '/admin',
    name: 'Admin',
    redirect: '/admin/dashboard',
    meta: {
      title: '后台管理',
      requiresAuth: true,
      roles: ['admin'],
    },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: {
          title: '仪表板',
          requiresAuth: true,
          roles: ['admin'],
        },
      },
      {
        path: 'products',
        name: 'AdminProductMgr',
        component: () => import('@/views/admin/ProductMgr.vue'),
        meta: {
          title: '商品管理',
          requiresAuth: true,
          roles: ['admin'],
        },
      },
      {
        path: 'orders',
        name: 'AdminOrderMgr',
        component: () => import('@/views/admin/OrderMgr.vue'),
        meta: {
          title: '订单管理',
          requiresAuth: true,
          roles: ['admin'],
        },
      },
      {
        path: 'users',
        name: 'AdminUserMgr',
        component: () => import('@/views/admin/UserMgr.vue'),
        meta: {
          title: '用户管理',
          requiresAuth: true,
          roles: ['admin'],
        },
      },
    ],
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue'),
    meta: {
      title: '页面不存在',
      requiresAuth: false,
    },
  },
]

export default routes
```

## 页面组件设计

### 1. 首页组件 (src/views/Home.vue)

```vue
<template>
  <div class="home">
    <!-- 轮播图 -->
    <el-carousel :interval="4000" type="card" height="400px">
      <el-carousel-item v-for="item in carouselItems" :key="item.id">
        <img :src="item.image" :alt="item.title" class="carousel-image" />
        <div class="carousel-content">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
          <el-button type="primary" size="large" @click="goToProducts">
            立即选购
          </el-button>
        </div>
      </el-carousel-item>
    </el-carousel>

    <!-- 热门分类 -->
    <section class="category-section">
      <div class="section-header">
        <h2>热门分类</h2>
        <el-button type="text" @click="goToAllCategories">
          查看全部 <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
      <div class="category-list">
        <div 
          v-for="category in categories" 
          :key="category.id"
          class="category-item"
          @click="goToCategory(category.id)"
        >
          <img :src="category.image" :alt="category.name" />
          <div class="category-info">
            <h3>{{ category.name }}</h3>
            <p>{{ category.count }}件商品</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 热门商品 -->
    <section class="product-section">
      <div class="section-header">
        <h2>热门商品</h2>
        <el-tabs v-model="activeTab" @tab-click="handleTabClick">
          <el-tab-pane label="热销榜" name="hot"></el-tab-pane>
          <el-tab-pane label="新品上市" name="new"></el-tab-pane>
          <el-tab-pane label="特价优惠" name="sale"></el-tab-pane>
        </el-tabs>
      </div>
      <div class="product-list">
        <ProductCard 
          v-for="product in products" 
          :key="product.id"
          :product="product"
          @click="goToProductDetail(product.id)"
        />
      </div>
      <div class="load-more">
        <el-button 
          type="primary" 
          :loading="loading" 
          @click="loadMoreProducts"
        >
          加载更多
        </el-button>
      </div>
    </section>

    <!-- 特色服务 -->
    <section class="service-section">
      <div class="service-list">
        <div class="service-item">
          <el-icon size="40"><Trophy /></el-icon>
          <div class="service-content">
            <h3>正品保障</h3>
            <p>100%正品，假一赔十</p>
          </div>
        </div>
        <div class="service-item">
          <el-icon size="40"><Truck /></el-icon>
          <div class="service-content">
            <h3>快速配送</h3>
            <p>全国包邮，急速送达</p>
          </div>
        </div>
        <div class="service-item">
          <el-icon size="40"><Refresh /></el-icon>
          <div class="service-content">
            <h3>7天退换</h3>
            <p>无忧退换，售后保障</p>
          </div>
        </div>
        <div class="service-item">
          <el-icon size="40"><Headset /></el-icon>
          <div class="service-content">
            <h3>客服支持</h3>
            <p>7×24小时在线服务</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  ArrowRight,
  Trophy,
  Truck,
  Refresh,
  Headset,
} from '@element-plus/icons-vue'
import ProductCard from '@/components/business/ProductCard.vue'
import { productApi } from '@/api/product'
import { categoryApi } from '@/api/category'

const router = useRouter()

// 响应式数据
const carouselItems = ref([
  {
    id: 1,
    image: '/images/banner1.jpg',
    title: '春季新品上市',
    description: '时尚男装，尽显绅士风度',
  },
  {
    id: 2,
    image: '/images/banner2.jpg',
    title: '夏季清凉特惠',
    description: '清爽夏日，舒适穿搭',
  },
  {
    id: 3,
    image: '/images/banner3.jpg',
    title: '秋季时尚搭配',
    description: '温暖秋季，时尚之选',
  },
])

const categories = ref([])
const products = ref([])
const activeTab = ref('hot')
const loading = ref(false)
const pageParams = ref({
  page: 1,
  size: 12,
  total: 0,
})

// 生命周期
onMounted(() => {
  loadCategories()
  loadProducts()
})

// 方法
const loadCategories = async () => {
  try {
    const data = await categoryApi.getHotCategories(6)
    categories.value = data
  } catch (error) {
    ElMessage.error('加载分类失败')
  }
}

const loadProducts = async () => {
  try {
    loading.value = true
    const params = {
      ...pageParams.value,
      type: activeTab.value,
    }
    const data = await productApi.getList(params)
    products.value = data.records
    pageParams.value.total = data.total
  } catch (error) {
    ElMessage.error('加载商品失败')
  } finally {
    loading.value = false
  }
}

const loadMoreProducts = async () => {
  if (loading.value || products.value.length >= pageParams.value.total) return
  
  pageParams.value.page++
  try {
    loading.value = true
    const params = {
      ...pageParams.value,
      type: activeTab.value,
    }
    const data = await productApi.getList(params)
    products.value = [...products.value, ...data.records]
  } catch (error) {
    ElMessage.error('加载更多商品失败')
    pageParams.value.page--
  } finally {
    loading.value = false
  }
}

const handleTabClick = () => {
  pageParams.value.page = 1
  loadProducts()
}

const goToProducts = () => {
  router.push('/products')
}

const goToAllCategories = () => {
  router.push('/categories')
}

const goToCategory = (categoryId) => {
  router.push(`/products?categoryId=${categoryId}`)
}

const goToProductDetail = (productId) => {
  router.push(`/products/${productId}`)
}
</script>

<style lang="scss" scoped>
.home {
  .carousel-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .carousel-content {
    position: absolute;
    bottom: 40px;
    left: 40px;
    color: white;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
    
    h3 {
      font-size: 32px;
      margin-bottom: 10px;
    }
    
    p {
      font-size: 18px;
      margin-bottom: 20px;
    }
  }
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 40px 0 20px;
    
    h2 {
      font-size: 24px;
      font-weight: bold;
      color: #333;
    }
  }
  
  .category-section {
    .category-list {
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 20px;
      
      .category-item {
        position: relative;
        border-radius: 8px;
        overflow: hidden;
        cursor: pointer;
        transition: transform 0.3s;
        
        &:hover {
          transform: translateY(-5px);
          
          img {
            transform: scale(1.1);
          }
        }
        
        img {
          width: 100%;
          height: 150px;
          object-fit: cover;
          transition: transform 0.3s;
        }
        
        .category-info {
          position: absolute;
          bottom: 0;
          left: 0;
          right: 0;
          background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
          color: white;
          padding: 10px;
          
          h3 {
            font-size: 16px;
            margin-bottom: 5px;
          }
          
          p {
            font-size: 12px;
            opacity: 0.8;
          }
        }
      }
    }
  }
  
  .product-section {
    .product-list {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
      margin-bottom: 30px;
    }
    
    .load-more {
      text-align: center;
    }
  }
  
  .service-section {
    margin: 60px 0;
    padding: 40px 0;
    background-color: #f8f9fa;
    
    .service-list {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 30px;
      
      .service-item {
        display: flex;
        align-items: center;
        justify-content: center;
        
        .el-icon {
          margin-right: 15px;
          color: #409EFF;
        }
        
        .service-content {
          h3 {
            font-size: 18px;
            margin-bottom: 5px;
            color: #333;
          }
          
          p {
            font-size: 14px;
            color: #666;
          }
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 1200px) {
  .home {
    .category-list {
      grid-template-columns: repeat(3, 1fr) !important;
    }
    
    .product-list {
      grid-template-columns: repeat(3, 1fr) !important;
    }
    
    .service-list {
      grid-template-columns: repeat(2, 1fr) !important;
    }
  }
}

@media (max-width: 768px) {
  .home {
    .category-list {
      grid-template-columns: repeat(2, 1fr) !important;
    }
    
    .product-list {
      grid-template-columns: repeat(2, 1fr) !important;
    }
    
    .service-list {
      grid-template-columns: 1fr !important;
    }
    
    .carousel-content {
      left: 20px !important;
      bottom: 20px !important;
      
      h3 {
        font-size: 24px !important;
      }
      
      p {
        font-size: 14px !important;
      }
    }
  }
}
</style>
```

### 2. 商品卡片组件 (src/components/business/ProductCard.vue)

```vue
<template>
  <div class="product-card" @click="$emit('click')">
    <div class="product-image">
      <img :src="product.mainImage" :alt="product.name" />
      <div v-if="product.isHot" class="hot-badge">热销</div>
      <div v-if="product.isNew" class="new-badge">新品</div>
      <div v-if="product.discount" class="discount-badge">
        {{ product.discount }}折
      </div>
    </div>
    <div class="product-info">
      <h3 class="product-name">{{ product.name }}</h3>
      <p class="product-subtitle">{{ product.subtitle }}</p>
      <div class="product-price">
        <span class="current-price">¥{{ product.price }}</span>
        <span v-if="product.originalPrice" class="original-price">
          ¥{{ product.originalPrice }}
        </span>
      </div>
      <div class="product-actions">
        <el-button 
          type="primary" 
          size="small" 
          @click.stop="addToCart"
          :loading="addingToCart"
        >
          加入购物车
        </el-button>
        <el-button 
          type="success" 
          size="small" 
          @click.stop