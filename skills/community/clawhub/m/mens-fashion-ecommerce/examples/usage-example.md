# 男装电商系统技能使用示例

## 示例场景

用户想要创建一个完整的男装电商平台，包含以下功能：
- 用户注册、登录、个人信息管理
- 商品分类浏览、搜索、详情查看
- 购物车功能
- 订单创建、支付、管理
- 后台管理系统

## 技能触发

用户输入：
```
请帮我创建一个男装电商系统，技术栈用SpringBoot3 + Vue3 + MySQL
```

## 技能执行流程

### 第一阶段：技术方案设计

**技能响应：**
```
好的，我将为您创建一个完整的男装电商系统。首先，让我为您设计详细的技术方案。

# 男装电商系统技术方案

## 1. 项目概述
- **项目名称**: 男装电商系统
- **技术栈**: SpringBoot3 + Vue3 + MySQL
- **架构模式**: 前后端分离
- **目标用户**: 男性消费者
- **核心功能**: 商品管理、用户管理、购物车、订单管理、支付集成

## 2. 系统架构设计

### 后端架构 (SpringBoot3)
- **框架**: SpringBoot 3.1.5
- **ORM**: MyBatis Plus 3.5.4
- **安全**: Spring Security + JWT
- **数据库**: MySQL 8.x
- **缓存**: Redis (可选)
- **API文档**: SpringDoc OpenAPI 3

### 前端架构 (Vue3)
- **框架**: Vue 3.3.8 + Composition API
- **UI库**: Element Plus 2.4.1
- **状态管理**: Pinia 2.1.7
- **路由**: Vue Router 4.2.5
- **构建工具**: Vite 5.0.8

### 数据库设计
- **用户管理**: user, user_address
- **商品管理**: product_category, product, product_sku
- **购物车**: cart
- **订单管理**: order, order_item
- **支付管理**: payment_record
- **库存管理**: inventory_record
- **营销管理**: coupon, user_coupon

## 3. 核心功能模块

### 3.1 用户管理模块
- 用户注册、登录、退出
- 个人信息管理
- 地址管理
- 安全设置

### 3.2 商品管理模块
- 商品分类管理
- 商品列表、搜索、筛选
- 商品详情展示
- 商品评价管理

### 3.3 购物车模块
- 添加商品到购物车
- 修改商品数量
- 选择/取消选择商品
- 批量操作

### 3.4 订单管理模块
- 创建订单
- 订单列表查询
- 订单详情查看
- 订单状态管理

### 3.5 支付模块
- 支付宝/微信支付集成
- 支付状态查询
- 支付回调处理

## 4. API接口设计

### 认证接口
- POST /api/auth/register - 用户注册
- POST /api/auth/login - 用户登录
- GET /api/auth/userinfo - 获取用户信息

### 商品接口
- GET /api/products - 获取商品列表
- GET /api/products/{id} - 获取商品详情
- POST /api/products - 创建商品 (管理员)

### 购物车接口
- GET /api/cart - 获取购物车列表
- POST /api/cart - 添加商品到购物车
- PUT /api/cart/{id} - 更新购物车商品

### 订单接口
- POST /api/orders - 创建订单
- GET /api/orders - 获取订单列表
- GET /api/orders/{id} - 获取订单详情

## 5. 项目结构

```
mens-fashion-ecommerce/
├── backend/                 # SpringBoot后端
│   ├── src/main/java/      # Java源代码
│   ├── src/main/resources/ # 配置文件
│   └── pom.xml            # Maven配置
├── frontend/               # Vue3前端
│   ├── src/               # Vue源代码
│   ├── public/            # 静态资源
│   └── package.json       # 项目配置
├── database/              # 数据库脚本
└── docs/                 # 项目文档
```

## 6. 部署方案

### 开发环境
- 后端: http://localhost:8080
- 前端: http://localhost:3000
- 数据库: MySQL本地实例

### 生产环境
- 服务器: 云服务器 (2核4G)
- 数据库: RDS MySQL
- 缓存: Redis云服务
- 部署方式: Docker容器化

## 7. 开发计划

### 第一阶段 (1-2周)
- 项目初始化
- 数据库设计实现
- 用户管理模块开发

### 第二阶段 (2-3周)
- 商品管理模块开发
- 购物车模块开发

### 第三阶段 (2-3周)
- 订单管理模块开发
- 支付模块集成

### 第四阶段 (1-2周)
- 系统测试
- 部署上线

---

**请确认以上技术方案是否满足您的需求？如果有任何修改意见，请告诉我。确认后我将开始生成完整的项目代码。**
```

### 第二阶段：代码生成（用户确认后）

**用户确认：**
```
方案很好，请开始生成代码。
```

**技能响应：**
```
好的，我将开始生成完整的男装电商系统代码。请稍等...

## 代码生成进度

### 1. 创建项目目录结构 ✓
- 创建主项目目录: mens-fashion-ecommerce
- 创建后端项目目录: backend/
- 创建前端项目目录: frontend/
- 创建文档目录: docs/

### 2. 生成后端项目文件 ✓
- 生成pom.xml (Maven配置)
- 生成application.yml (SpringBoot配置)
- 生成EcommerceApplication.java (启动类)
- 生成统一响应类: Result.java
- 生成业务异常类: BusinessException.java
- 生成全局异常处理器: GlobalExceptionHandler.java

### 3. 生成数据库脚本 ✓
- 生成数据库初始化脚本: database/init.sql
- 包含12张核心表结构
- 包含初始数据插入
- 包含索引优化脚本

### 4. 生成前端项目文件 ✓
- 生成package.json (项目配置)
- 生成vite.config.js (构建配置)
- 生成main.js (入口文件)
- 生成App.vue (根组件)
- 生成样式变量文件: variables.scss
- 生成全局样式文件: global.scss

### 5. 生成核心模块代码

#### 5.1 用户管理模块 ✓
- 实体类: User.java, UserAddress.java
- 数据访问层: UserMapper.java, UserAddressMapper.java
- 服务层: UserService.java, AuthService.java
- 控制层: AuthController.java, UserController.java
- 前端页面: Login.vue, Register.vue, Profile.vue

#### 5.2 商品管理模块 ✓
- 实体类: ProductCategory.java, Product.java, ProductSku.java
- 数据访问层: ProductMapper.java, CategoryMapper.java
- 服务层: ProductService.java, CategoryService.java
- 控制层: ProductController.java, CategoryController.java
- 前端页面: ProductList.vue, ProductDetail.vue, Category.vue

#### 5.3 购物车模块 ✓
- 实体类: Cart.java
- 数据访问层: CartMapper.java
- 服务层: CartService.java
- 控制层: CartController.java
- 前端页面: Cart.vue

#### 5.4 订单管理模块 ✓
- 实体类: Order.java, OrderItem.java
- 数据访问层: OrderMapper.java, OrderItemMapper.java
- 服务层: OrderService.java
- 控制层: OrderController.java
- 前端页面: OrderList.vue, OrderDetail.vue, OrderConfirm.vue

#### 5.5 支付模块 ✓
- 实体类: PaymentRecord.java
- 数据访问层: PaymentMapper.java
- 服务层: PaymentService.java
- 控制层: PaymentController.java
- 支付接口: AlipayService.java, WechatPayService.java

### 6. 生成工具类和配置 ✓
- JWT工具类: JwtUtil.java
- Redis工具类: RedisUtil.java
- 文件上传工具: FileUploadUtil.java
- Spring Security配置: SecurityConfig.java
- MyBatis Plus配置: MyBatisPlusConfig.java
- 跨域配置: CorsConfig.java

### 7. 生成API文档 ✓
- 集成Swagger UI
- 生成API接口文档
- 访问地址: http://localhost:8080/swagger-ui.html

### 8. 生成部署文档 ✓
- 开发环境部署指南
- 生产环境部署指南
- Docker部署配置
- Nginx配置示例

## 项目生成完成！

已成功生成完整的男装电商系统项目，包含：

### 后端项目 (SpringBoot3)
- 12个核心实体类
- 15个数据访问接口
- 10个服务类
- 8个控制器
- 完整的配置和工具类

### 前端项目 (Vue3)
- 10个页面组件
- 8个业务组件
- 完整的路由配置
- 状态管理配置
- API接口封装

### 数据库设计
- 12张核心表
- 完整的索引优化
- 初始数据脚本

### 项目文档
- API接口文档
- 数据库设计文档
- 部署指南
- 开发指南

## 快速开始指南

### 1. 环境准备
```bash
# 安装Java 17
brew install openjdk@17

# 安装Node.js 18
brew install node@18

# 安装MySQL 8
brew install mysql@8.0
```

### 2. 启动项目
```bash
# 克隆项目
git clone <项目地址>
cd mens-fashion-ecommerce

# 初始化数据库
mysql -u root -p < database/init.sql

# 启动后端
cd backend
mvn spring-boot:run

# 启动前端 (新终端)
cd frontend
npm install
npm run dev
```

### 3. 访问系统
- 前端地址: http://localhost:3000
- 后端API: http://localhost:8080
- API文档: http://localhost:8080/swagger-ui.html

### 4. 测试账号
- 管理员: admin / admin123
- 普通用户: testuser / test123

## 下一步建议

1. **功能测试**: 测试所有核心功能是否正常工作
2. **性能优化**: 根据实际需求优化数据库查询和缓存策略
3. **安全加固**: 配置HTTPS、防火墙等安全措施
4. **监控部署**: 添加系统监控和日志分析
5. **扩展开发**: 根据业务需求添加新功能模块

---

项目已生成完成！您可以开始进行功能测试和定制开发。如果有任何问题或需要进一步的帮助，请随时告诉我。
```

## 技能输出文件示例

### 1. 后端实体类示例 (User.java)
```java
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("user")
public class User implements UserDetails {
    
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;
    
    @TableField("username")
    private String username;
    
    @TableField("password")
    private String password;
    
    @TableField("email")
    private String email;
    
    @TableField("phone")
    private String phone;
    
    // ... 其他字段和方法
}
```

### 2. 前端页面组件示例 (Login.vue)
```vue
<template>
  <div class="login-container">
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules">
      <el-form-item prop="username">
        <el-input v-model="loginForm.username" placeholder="用户名/邮箱/手机号" />
      </el-form-item>
      <el-form-item prop="password">
        <el-input v-model="loginForm.password" type="password" placeholder="密码" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleLogin" :loading="loading">
          登录
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/modules/auth'

const router = useRouter()
const authStore = useAuthStore()

const loginForm = ref({
  username: '',
  password: '',
})

const loading = ref(false)

const handleLogin = async () => {
  try {
    loading.value = true
    await authStore.login(loginForm.value)
    router.push('/')
  } catch (error) {
    console.error('登录失败:', error)
  } finally {
    loading.value = false
  }
}
</script>
```

### 3. 数据库脚本示例 (init.sql)
```sql
-- 用户表
CREATE TABLE `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(255) NOT NULL COMMENT '密码',
  `email` varchar(100) DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  -- ... 其他字段
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 插入测试数据
INSERT INTO `user` (`username`, `password`, `email`, `phone`) VALUES
('admin', '$2a$10$N.zmdr9k7uOCQb376NoUnu...', 'admin@example.com', '13800138000'),
('testuser', '$2a$10$N.zmdr9k7uOCQb376NoUnu...', 'test@example.com', '13800138001');
```

## 技能优势

1. **完整性**: 生成完整的、可运行的项目
2. **规范性**: 代码符合企业级开发规范
3. **可扩展性**: 模块化设计，易于扩展
4. **文档齐全**: 提供完整的技术文档
5. **现代化技术栈**: 使用最新的技术框架和工具

## 适用场景

1. **创业项目**: 快速搭建电商平台原型
2. **教学演示**: 学习现代Web开发技术栈
3. **企业项目**: 作为基础框架进行二次开发
4. **个人项目**: 实践全栈开发技能

---

通过这个技能，用户可以快速获得一个功能完整、代码规范、文档齐全的男装电商系统项目，大大缩短开发周期，降低开发成本。