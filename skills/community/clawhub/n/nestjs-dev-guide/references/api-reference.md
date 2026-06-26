# NestJS API Deep Reference

## Complete Decorator Cheat Sheet

### HTTP Method Decorators
```ts
@Get()        @Post()       @Put()
@Delete()     @Patch()      @Options()
@Head()       @All()
```

### Parameter Decorators
```ts
@Param(key?: string)       // req.params / req.params[key]
@Body(key?: string)        // req.body / req.body[key]
@Query(key?: string)       // req.query / req.query[key]
@Headers(name?: string)    // req.headers / req.headers[name]
@Req()                     // req (Express) / request (Fastify)
@Res()                     // res — requires manual response handling
@Next()                    // Express next()
@Session()                 // req.session
@Ip()                      // req.ip
@HostParam()               // req.hosts dynamic subdomain parameters
@UploadedFile()            // File upload
@UploadedFiles()           // Multiple file upload
```

### Response Control Decorators
```ts
@HttpCode(204)             // Custom status code
@Header('key', 'value')    // Custom response header
@Redirect('url', 302)      // Redirect
```

### Binding Decorators
```ts
@UsePipes()                // Bind pipe
@UseGuards()               // Bind guard
@UseInterceptors()         // Bind interceptor
@UseFilters()              // Bind exception filter
@SetMetadata('key', 'val') // Set custom metadata
@Render('view')            // MVC view rendering
```

## Platform Configuration

```ts
// Express (default)
const app = await NestFactory.create<NestExpressApplication>(AppModule);

// Fastify
const app = await NestFactory.create<NestFastifyApplication>(
  AppModule,
  new FastifyAdapter()
);

// Configuration options
const app = await NestFactory.create(AppModule, {
  abortOnError: false,     // Do not exit on startup error (default exit code 1)
  logger: ['error', 'warn', 'log'],
  cors: true,              // or { origin: '*', methods: 'GET,POST' }
});
```

### Express Specific
```ts
app.set('query parser', 'extended');  // Support nested query parameters
app.useStaticAssets(join(__dirname, '..', 'public'));
app.setBaseViewsDir(join(__dirname, '..', 'views'));
app.setViewEngine('hbs');
```

## Custom Providers Complete Syntax

```ts
// useClass — most common
{ provide: CatsService, useClass: CatsService }

// useValue — constants, mocks, config objects
{ provide: 'CONFIG', useValue: { host: 'localhost' } }

// useFactory — dynamic creation
{
  provide: 'DATABASE_CONNECTION',
  useFactory: async (configService: ConfigService) => {
    return await createConnection(configService.get('DB_URL'));
  },
  inject: [ConfigService],
}

// useExisting — alias
{ provide: 'AliasService', useExisting: CatsService }

// Non-class Token (inject with @Inject())
{ provide: 'CACHE_MANAGER', useClass: CacheManager }
// Injection:
constructor(@Inject('CACHE_MANAGER') private cacheManager) {}
```

## Dynamic Module Complete Example

```ts
interface DatabaseOptions {
  host: string; port: number; username: string; password: string;
}

@Module({})
export class DatabaseModule {
  static forRoot(options: DatabaseOptions): DynamicModule {
    return {
      module: DatabaseModule,
      global: false,
      providers: [
        { provide: 'DATABASE_OPTIONS', useValue: options },
        { provide: 'DATABASE_CONNECTION', useFactory: (opts) => createConnection(opts), inject: ['DATABASE_OPTIONS'] },
      ],
      exports: ['DATABASE_CONNECTION'],
    };
  }
}

// Usage
@Module({ imports: [DatabaseModule.forRoot({ host: 'localhost', port: 5432, username: 'postgres', password: 'pass' })] })
```

## ValidationPipe Complete Options

```ts
new ValidationPipe({
  whitelist: true,              // Strip properties without decorators
  forbidNonWhitelisted: true,   // Throw 400 if non-whitelisted properties exist
  transform: true,              // Auto type conversion
  disableErrorMessages: false,  // Can disable detailed errors in production
  errorHttpStatusCode: 400,     // Status code to throw on error
  exceptionFactory: (errors) => new BadRequestException(errors),
  stopAtFirstError: true,       // Stop at first error
  groups: ['create'],           // Validation groups
  always: true,                 // Default value for decorator always option
  errorFormat: 'grouped',       // 'list' | 'grouped'
  skipMissingProperties: false,
  skipNullProperties: false,
  skipUndefinedProperties: false,
  validationError: { target: false, value: false },
})
```

## Common class-validator Decorators

```ts
// General
@IsOptional()         @IsNotEmpty()         @IsDefined()
@Equals('val')        @NotEquals('val')     @IsIn(['a','b'])

// Type
@IsString()           @IsNumber()           @IsBoolean()
@IsDate()             @IsEnum(MyEnum)       @IsInt()
@IsArray()            @IsObject()

// String
@Length(1, 50)        @MinLength(3)         @MaxLength(100)
@Contains('val')      @Matches(/regex/)     @IsEmail()
@IsUrl()              @IsUUID()             @IsJSON()
@IsAlpha()            @IsAlphanumeric()     @IsBase64()
@IsLowercase()        @IsUppercase()

// Number
@Min(0)               @Max(100)             @IsPositive()
@IsNegative()         @IsDivisibleBy(5)

// Nested
@ValidateNested()     @ArrayMinSize(1)      @ArrayMaxSize(10)
@ArrayNotEmpty()      @ArrayUnique()
```

## ExecutionContext Details

```ts
// Get HTTP context
const ctx = context.switchToHttp();
const request = ctx.getRequest<Request>();
const response = ctx.getResponse<Response>();
const next = ctx.getNext();

// Get WebSocket context
const wsCtx = context.switchToWs();
const client = wsCtx.getClient();
const data = wsCtx.getData();

// Get RPC context
const rpcCtx = context.switchToRpc();
const rpcData = rpcCtx.getData();

// Get metadata
context.getClass()      // Controller class
context.getHandler()    // Route handler method reference
context.getType()       // 'http' | 'ws' | 'rpc'
```

## Reflector Usage

```ts
// Read method-level metadata
const roles = reflector.get<string[]>('roles', context.getHandler());

// Read class-level metadata
const classRoles = reflector.get<string[]>('roles', context.getClass());

// Read both method and class (method overrides class)
const allRoles = reflector.getAllAndOverride<string[]>('roles', [
  context.getHandler(),
  context.getClass(),
]);

// Merge method and class metadata
const merged = reflector.getAllAndMerge<string[]>('roles', [
  context.getHandler(),
  context.getClass(),
]);
```

## Response Mode Comparison

```ts
// Nest standard mode (recommended)
@Get()
findAll(): Cat[] {
  return this.catsService.findAll();  // Nest auto-serializes
}

// Library-specific mode (not recommended — loses interceptor/pipe support)
@Get()
findAll(@Res() res: Response) {
  res.status(200).json([]);
}

// Hybrid mode (passthrough — manual parts + Nest handles the rest)
@Get()
findAll(@Res({ passthrough: true }) res: Response) {
  res.cookie('key', 'value');  // Manual cookie setting
  return [];                    // Nest handles return
}
```

## Global Prefix

```ts
app.setGlobalPrefix('api/v1');
// Exclude specific routes
app.setGlobalPrefix('api', { exclude: ['health', 'metrics'] });
```

## Platform-specific Pipe Shortcuts

```ts
// Parameter-level built-in pipes
@Param('id', ParseIntPipe) id: number
@Param('id', new ParseIntPipe({ errorHttpStatusCode: 400 }))
@Query('ids', new ParseArrayPipe({ items: Number, separator: ',' })) ids: number[]
@Query('filter', new ParseBoolPipe({ optional: true })) filter?: boolean
```

## Middleware Additional Usage

```ts
// Exclude routes
consumer.apply(LoggerMiddleware)
  .exclude({ path: 'cats', method: RequestMethod.GET }, 'cats/(.*)')
  .forRoutes(CatsController);

// Global middleware (main.ts)
app.use(helmet());
app.use(cors());
app.use(compression());
```

## TypeORM Integration Key Points

```ts
// Entity
@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  email: string;

  @Column({ select: false })  // Not returned by default in queries
  password: string;

  @CreateDateColumn()
  createdAt: Date;
}

// Repository injection
@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User) private userRepo: Repository<User>,
  ) {}

  findAll(): Promise<User[]> {
    return this.userRepo.find({ relations: ['posts'] });
  }
}
```

## Lifecycle Hooks

```ts
// Module-level
@Injectable()
export class MyService implements OnModuleInit, OnModuleDestroy, OnApplicationBootstrap, OnApplicationShutdown {
  onModuleInit() {}
  onModuleDestroy() {}
  onApplicationBootstrap() {}
  onApplicationShutdown(signal?: string) {}
}