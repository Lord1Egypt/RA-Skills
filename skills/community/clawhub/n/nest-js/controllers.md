# NestJS Controllers

## Basics
```typescript
@Controller('users') // prefix: /users
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()           // GET /users
  findAll() { return this.usersService.findAll(); }

  @Get(':id')      // GET /users/:id
  findOne(@Param('id', ParseIntPipe) id: number) {
    return this.usersService.findOne(id);
  }

  @Post()          // POST /users
  @HttpCode(201)
  create(@Body() dto: CreateUserDto) {
    return this.usersService.create(dto);
  }
}
```

## Parameter Decorators

| Decorator | Express equivalent |
|-----------|-------------------|
| `@Body(key?)` | `req.body` / `req.body[key]` |
| `@Param(key?)` | `req.params` / `req.params[key]` |
| `@Query(key?)` | `req.query` / `req.query[key]` |
| `@Headers(key?)` | `req.headers` / `req.headers[key]` |
| `@Ip()` | `req.ip` |
| `@Req()` | `req` (ties you to Express — avoid) |
| `@Res()` | `res` (⚠️ see trap below) |

## Common Traps

### `@Res()` Takes Over Response Handling
```typescript
// ❌ Nest no longer serializes return value — you must call res.json() yourself
@Get()
findAll(@Res() res: Response) {
  return this.service.findAll(); // SILENTLY IGNORED, request hangs
}

// ✅ passthrough mode — Nest still handles response, but you can set headers/status
@Get()
findAll(@Res({ passthrough: true }) res: Response) {
  res.header('X-Custom', 'value');
  return this.service.findAll(); // Nest serializes this normally
}
```

### Route Order Matters
```typescript
// ❌ ':id' matches 'profile' — GET /users/profile hits findOne('profile')
@Get(':id')
findOne(@Param('id') id: string) {}

@Get('profile')
getProfile() {}

// ✅ Specific routes BEFORE parameterized ones
@Get('profile')
getProfile() {}

@Get(':id')
findOne(@Param('id') id: string) {}
```

### API Versioning
```typescript
// In main.ts
app.enableVersioning({ type: VersioningType.URI }); // /v1/users

// On controller or route
@Controller({ path: 'users', version: '1' })

// Or per-route
@Version('2')
@Get()
findAllV2() {}
```

### File Upload
```typescript
@Post('upload')
@UseInterceptors(FileInterceptor('file'))
uploadFile(@UploadedFile() file: Express.Multer.File) {
  // file.buffer, file.originalname, file.mimetype
}

// With validation
@UploadedFile(
  new ParseFilePipe({
    validators: [
      new MaxFileSizeValidator({ maxSize: 5 * 1024 * 1024 }),
      new FileTypeValidator({ fileType: 'image/png' }),
    ],
  }),
)
```

### Response Serialization
```typescript
// Use ClassSerializerInterceptor to auto-exclude fields
@Entity()
export class User {
  @Exclude()
  password: string; // stripped from all responses

  @Expose()
  get fullName() { return `${this.first} ${this.last}`; }
}

// Enable globally or per-controller
@UseInterceptors(ClassSerializerInterceptor)
@Controller('users')
export class UsersController {}
```

### Custom Decorators
```typescript
// Extract user from request (set by AuthGuard)
export const CurrentUser = createParamDecorator(
  (data: string, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;
    return data ? user?.[data] : user;
  },
);

// Usage: @CurrentUser() user: User
// Usage: @CurrentUser('email') email: string
```

### Combining Decorators
```typescript
// Bundle common decorators
export function Auth(...roles: Role[]) {
  return applyDecorators(
    SetMetadata('roles', roles),
    UseGuards(AuthGuard, RolesGuard),
    ApplyDecorators(ApiOperation({ summary: 'Protected endpoint' })),
  );
}

// Usage: @Auth(Role.Admin)
```
