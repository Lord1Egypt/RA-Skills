# 后端架构详细设计

## 项目结构

```
mens-fashion-ecommerce-backend/
├── src/main/java/com/mensfashion/ecommerce/
│   ├── config/                    # 配置类
│   │   ├── SecurityConfig.java    # 安全配置
│   │   ├── MyBatisPlusConfig.java # MyBatis Plus配置
│   │   ├── RedisConfig.java       # Redis配置（可选）
│   │   └── SwaggerConfig.java     # Swagger配置
│   ├── controller/                # 控制器层
│   │   ├── auth/                  # 认证相关
│   │   ├── user/                  # 用户管理
│   │   ├── product/               # 商品管理
│   │   ├── cart/                  # 购物车
│   │   ├── order/                 # 订单管理
│   │   ├── payment/               # 支付管理
│   │   └── admin/                 # 后台管理
│   ├── service/                   # 服务层
│   │   ├── impl/                  # 服务实现
│   │   └── *.java                 # 服务接口
│   ├── mapper/                    # 数据访问层
│   ├── entity/                    # 实体类
│   ├── dto/                       # 数据传输对象
│   │   ├── request/               # 请求DTO
│   │   └── response/              # 响应DTO
│   ├── vo/                        # 视图对象
│   ├── enums/                     # 枚举类
│   ├── exception/                 # 异常处理
│   │   ├── GlobalExceptionHandler.java
│   │   └── BusinessException.java
│   ├── utils/                     # 工具类
│   │   ├── JwtUtil.java           # JWT工具
│   │   ├── RedisUtil.java         # Redis工具
│   │   └── CommonUtil.java        # 通用工具
│   └── EcommerceApplication.java  # 启动类
├── src/main/resources/
│   ├── application.yml            # 主配置文件
│   ├── application-dev.yml        # 开发环境配置
│   ├── application-prod.yml       # 生产环境配置
│   ├── mapper/                    # MyBatis XML映射文件
│   └── static/                    # 静态资源
└── pom.xml                        # Maven配置
```

## 核心配置

### 1. 数据库配置 (application.yml)

```yaml
spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/mens_fashion_db?useUnicode=true&characterEncoding=utf-8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: 123456
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000

  # Redis配置（可选）
  redis:
    host: localhost
    port: 6379
    password: 
    database: 0
    timeout: 3000ms
    lettuce:
      pool:
        max-active: 20
        max-idle: 10
        min-idle: 5
        max-wait: 3000ms
```

### 2. MyBatis Plus配置

```java
@Configuration
@MapperScan("com.mensfashion.ecommerce.mapper")
public class MyBatisPlusConfig {
    
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        // 分页插件
        interceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.MYSQL));
        // 乐观锁插件
        interceptor.addInnerInterceptor(new OptimisticLockerInnerInterceptor());
        return interceptor;
    }
    
    @Bean
    public ConfigurationCustomizer configurationCustomizer() {
        return configuration -> configuration.setUseGeneratedKeys(true);
    }
}
```

### 3. Spring Security配置

```java
@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class SecurityConfig {
    
    @Autowired
    private JwtAuthenticationTokenFilter jwtAuthenticationTokenFilter;
    
    @Autowired
    private AccessDeniedHandlerImpl accessDeniedHandler;
    
    @Autowired
    private AuthenticationEntryPointImpl authenticationEntryPoint;
    
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
    
    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            // 禁用CSRF
            .csrf().disable()
            // 会话管理
            .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            .and()
            // 授权配置
            .authorizeHttpRequests(auth -> auth
                // 公开接口
                .requestMatchers(
                    "/api/auth/**",
                    "/api/products/public/**",
                    "/swagger-ui/**",
                    "/v3/api-docs/**",
                    "/webjars/**"
                ).permitAll()
                // 需要认证的接口
                .anyRequest().authenticated()
            )
            // 添加JWT过滤器
            .addFilterBefore(jwtAuthenticationTokenFilter, UsernamePasswordAuthenticationFilter.class)
            // 异常处理
            .exceptionHandling()
                .accessDeniedHandler(accessDeniedHandler)
                .authenticationEntryPoint(authenticationEntryPoint);
        
        return http.build();
    }
    
    @Bean
    public WebSecurityCustomizer webSecurityCustomizer() {
        return web -> web.ignoring().requestMatchers("/error");
    }
}
```

### 4. JWT工具类

```java
@Component
public class JwtUtil {
    
    @Value("${jwt.secret}")
    private String secret;
    
    @Value("${jwt.expiration}")
    private Long expiration;
    
    /**
     * 生成token
     */
    public String generateToken(UserDetails userDetails) {
        Map<String, Object> claims = new HashMap<>();
        claims.put("username", userDetails.getUsername());
        claims.put("created", new Date());
        
        return Jwts.builder()
                .setClaims(claims)
                .setSubject(userDetails.getUsername())
                .setIssuedAt(new Date())
                .setExpiration(generateExpirationDate())
                .signWith(SignatureAlgorithm.HS512, secret)
                .compact();
    }
    
    /**
     * 验证token
     */
    public Boolean validateToken(String token, UserDetails userDetails) {
        final String username = getUsernameFromToken(token);
        return (username.equals(userDetails.getUsername()) && !isTokenExpired(token));
    }
    
    /**
     * 从token中获取用户名
     */
    public String getUsernameFromToken(String token) {
        return getClaimsFromToken(token).getSubject();
    }
    
    /**
     * 从token中获取Claims
     */
    public Claims getClaimsFromToken(String token) {
        return Jwts.parser()
                .setSigningKey(secret)
                .parseClaimsJws(token)
                .getBody();
    }
    
    /**
     * 生成过期时间
     */
    private Date generateExpirationDate() {
        return new Date(System.currentTimeMillis() + expiration * 1000);
    }
    
    /**
     * 判断token是否过期
     */
    private Boolean isTokenExpired(String token) {
        final Date expiration = getExpirationDateFromToken(token);
        return expiration.before(new Date());
    }
    
    /**
     * 获取token过期时间
     */
    public Date getExpirationDateFromToken(String token) {
        return getClaimsFromToken(token).getExpiration();
    }
}
```

## 核心实体类设计

### 1. 用户实体 (User)

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
    
    @TableField("avatar")
    private String avatar;
    
    @TableField("gender")
    private Integer gender; // 0:未知, 1:男, 2:女
    
    @TableField("birthday")
    private Date birthday;
    
    @TableField("status")
    private Integer status; // 0:禁用, 1:正常
    
    @TableField("last_login_time")
    private Date lastLoginTime;
    
    @TableField("create_time")
    private Date createTime;
    
    @TableField("update_time")
    private Date updateTime;
    
    @TableField(exist = false)
    private List<GrantedAuthority> authorities;
    
    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return authorities;
    }
    
    @Override
    public boolean isAccountNonExpired() {
        return true;
    }
    
    @Override
    public boolean isAccountNonLocked() {
        return status == 1;
    }
    
    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }
    
    @Override
    public boolean isEnabled() {
        return status == 1;
    }
}
```

### 2. 商品实体 (Product)

```java
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("product")
public class Product {
    
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;
    
    @TableField("category_id")
    private Long categoryId;
    
    @TableField("name")
    private String name;
    
    @TableField("subtitle")
    private String subtitle;
    
    @TableField("main_image")
    private String mainImage;
    
    @TableField("sub_images")
    private String subImages; // JSON数组格式
    
    @TableField("detail")
    private String detail;
    
    @TableField("price")
    private BigDecimal price;
    
    @TableField("stock")
    private Integer stock;
    
    @TableField("status")
    private Integer status; // 0:下架, 1:上架
    
    @TableField("is_hot")
    private Boolean isHot;
    
    @TableField("is_new")
    private Boolean isNew;
    
    @TableField("sort_order")
    private Integer sortOrder;
    
    @TableField("create_time")
    private Date createTime;
    
    @TableField("update_time")
    private Date updateTime;
}
```

### 3. 订单实体 (Order)

```java
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("`order`")
public class Order {
    
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;
    
    @TableField("order_no")
    private String orderNo;
    
    @TableField("user_id")
    private Long userId;
    
    @TableField("total_price")
    private BigDecimal totalPrice;
    
    @TableField("status")
    private Integer status; // 0:已取消, 1:未付款, 2:已付款, 3:已发货, 4:交易成功, 5:交易关闭
    
    @TableField("payment_type")
    private Integer paymentType; // 1:支付宝, 2:微信
    
    @TableField("payment_no")
    private String paymentNo;
    
    @TableField("payment_time")
    private Date paymentTime;
    
    @TableField("shipping_code")
    private String shippingCode;
    
    @TableField("shipping_time")
    private Date shippingTime;
    
    @TableField("receive_time")
    private Date receiveTime;
    
    @TableField("close_time")
    private Date closeTime;
    
    @TableField("create_time")
    private Date createTime;
    
    @TableField("update_time")
    private Date updateTime;
    
    @TableField("address_id")
    private Long addressId;
    
    @TableField("remark")
    private String remark;
}
```

## 服务层设计模式

### 1. 基础服务接口

```java
public interface BaseService<T> {
    
    /**
     * 根据ID查询
     */
    T getById(Long id);
    
    /**
     * 查询所有
     */
    List<T> listAll();
    
    /**
     * 分页查询
     */
    Page<T> listPage(Page<T> page);
    
    /**
     * 保存
     */
    boolean save(T entity);
    
    /**
     * 更新
     */
    boolean updateById(T entity);
    
    /**
     * 删除
     */
    boolean removeById(Long id);
    
    /**
     * 批量删除
     */
    boolean removeByIds(List<Long> ids);
}
```

### 2. 商品服务示例

```java
public interface ProductService extends BaseService<Product> {
    
    /**
     * 根据分类查询商品
     */
    List<Product> listByCategoryId(Long categoryId);
    
    /**
     * 搜索商品
     */
    Page<Product> search(String keyword, Page<Product> page);
    
    /**
     * 获取热门商品
     */
    List<Product> listHotProducts(Integer limit);
    
    /**
     * 获取新品
     */
    List<Product> listNewProducts(Integer limit);
    
    /**
     * 更新库存
     */
    boolean updateStock(Long productId, Integer quantity);
    
    /**
     * 检查库存
     */
    boolean checkStock(Long productId, Integer quantity);
}
```

## 统一响应格式

```java
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Result<T> {
    
    private Integer code;
    private String message;
    private T data;
    private Long timestamp;
    
    public static <T> Result<T> success() {
        return new Result<>(200, "success", null, System.currentTimeMillis());
    }
    
    public static <T> Result<T> success(T data) {
        return new Result<>(200, "success", data, System.currentTimeMillis());
    }
    
    public static <T> Result<T> success(String message, T data) {
        return new Result<>(200, message, data, System.currentTimeMillis());
    }
    
    public static <T> Result<T> error(Integer code, String message) {
        return new Result<>(code, message, null, System.currentTimeMillis());
    }
    
    public static <T> Result<T> error(String message) {
        return new Result<>(500, message, null, System.currentTimeMillis());
    }
}
```

## 全局异常处理

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);
    
    /**
     * 处理业务异常
     */
    @ExceptionHandler(BusinessException.class)
    public Result<?> handleBusinessException(BusinessException e) {
        logger.error("业务异常: {}", e.getMessage(), e);
        return Result.error(e.getCode(), e.getMessage());
    }
    
    /**
     * 处理认证异常
     */
    @ExceptionHandler(AuthenticationException.class)
    public Result<?> handleAuthenticationException(AuthenticationException e) {
        logger.error("认证异常: {}", e.getMessage(), e);
        return Result.error(401, "认证失败: " + e.getMessage());
    }
    
    /**
     * 处理权限异常
     */
    @ExceptionHandler(AccessDeniedException.class)
    public Result<?> handleAccessDeniedException(AccessDeniedException e) {
        logger.error("权限异常: {}", e.getMessage(), e);
        return Result.error(403, "权限不足");
    }
    
    /**
     * 处理其他异常
     */
    @ExceptionHandler(Exception.class)
    public Result<?> handleException(Exception e) {
        logger.error("系统异常: {}", e.getMessage(), e);
        return Result.error(500, "系统异常: " + e.getMessage());
    }
}
```

## API设计规范

### 1. RESTful API设计原则

- 使用名词复数形式表示资源
- 使用HTTP方法表示操作类型
- 使用状态码表示操作结果
- 使用查询参数进行过滤、排序、分页

### 2. 接口示例

```
# 用户相关
GET    /api/users           # 获取用户列表
GET    /api/users/{id}      # 获取用户详情
POST   /api/users           # 创建用户
PUT    /api/users/{id}      # 更新用户
DELETE /api/users/{id}      # 删除用户

# 商品相关
GET    /api/products        # 获取商品列表
GET    /api/products/{id}   # 获取商品详情
POST   /api/products        # 创建商品
PUT    /api/products/{id}   # 更新商品
DELETE /api/products/{id}   # 删除商品

# 订单相关
GET    /api/orders          # 获取订单列表
GET    /api/orders/{id}     # 获取订单详情
POST   /api/orders          # 创建订单
PUT    /api/orders/{id}     # 更新订单状态
```

### 3. 分页参数

```json
{
  "page": 1,      // 当前页码
  "size": 10,     // 每页大小
  "total": 100,   // 总记录数
  "pages": 10,    // 总页数
  "records": []   // 数据列表
}
```

## 性能优化建议

### 1. 数据库优化
- 为常用查询字段添加索引
- 避免SELECT *，只查询需要的字段
- 使用连接查询代替多次查询
- 合理使用数据库缓存

### 2. 应用层优化
- 使用Redis缓存热点数据
- 使用连接池管理数据库连接
- 异步处理耗时操作
- 使用消息队列解耦系统

### 3. 代码优化
- 使用DTO减少数据传输量
- 使用懒加载避免N+1查询
- 使用批量操作减少数据库交互
