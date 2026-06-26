# NestJS Validation & DTOs

## Setup
```bash
npm install class-validator class-transformer
```
Both packages required. `class-validator` defines rules, `class-transformer` handles plain-object → class-instance conversion.

## DTO Pattern
```typescript
import { IsString, IsEmail, IsOptional, MinLength, IsEnum, ValidateNested, Type } from 'class-validator';

export class CreateUserDto {
  @IsString()
  @MinLength(2)
  name: string;

  @IsEmail()
  email: string;

  @IsOptional()
  @IsString()
  bio?: string;

  @IsEnum(Role)
  role: Role;

  @ValidateNested()
  @Type(() => AddressDto) // ⚠️ Required for nested object validation
  address: AddressDto;
}
```

## Common Traps

### `class-transformer` Not Installed
- `ValidationPipe` with `transform: true` silently fails — body stays plain object
- Nested `@ValidateNested()` doesn't work without `@Type()` decorator
- Install both: `npm install class-validator class-transformer`

### Missing `@Type()` on Nested Objects
```typescript
// ❌ Nested validation NEVER runs — address is just a plain object
@ValidateNested()
address: AddressDto;

// ✅ @Type tells class-transformer which class to instantiate
@ValidateNested()
@Type(() => AddressDto)
address: AddressDto;
```

### Arrays of Nested Objects
```typescript
@ValidateNested({ each: true })
@Type(() => ItemDto)
items: ItemDto[];
```

### Partial Updates (PATCH)
```typescript
// PartialType makes all fields optional, preserving validation rules
import { PartialType } from '@nestjs/mapped-types';
// or from @nestjs/swagger if using Swagger

export class UpdateUserDto extends PartialType(CreateUserDto) {}
```
- `PartialType` — all optional
- `PickType(CreateUserDto, ['name', 'email'])` — select specific fields
- `OmitType(CreateUserDto, ['password'])` — exclude specific fields
- `IntersectionType(A, B)` — combine two DTOs

### Whitelist vs ForbidNonWhitelisted
```typescript
new ValidationPipe({
  whitelist: true,              // silently strips unknown properties
  forbidNonWhitelisted: true,   // throws 400 if unknown properties present
})
```
- `whitelist: true` alone silently drops extra fields — attacker sends `{ role: 'admin' }` and it's stripped
- Add `forbidNonWhitelisted` to reject the request entirely

### Transform Mode
```typescript
new ValidationPipe({
  transform: true,
  transformOptions: {
    enableImplicitConversion: true, // @Query('page') page: number → auto parseInt
  },
})
```
- Without `transform: true`, handler receives plain object, not DTO class instance
- `enableImplicitConversion` converts based on TypeScript type metadata — strings to numbers/booleans in `@Query()`

### Custom Validation
```typescript
// Custom decorator
export function IsStrongPassword(validationOptions?: ValidationOptions) {
  return function (object: Object, propertyName: string) {
    registerDecorator({
      name: 'isStrongPassword',
      target: object.constructor,
      propertyName,
      options: validationOptions,
      validator: {
        validate(value: string) {
          return /^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%]).{8,}$/.test(value);
        },
        defaultMessage() {
          return 'Password too weak';
        },
      },
    });
  };
}
```

### Validation Groups
```typescript
export class UserDto {
  @IsOptional({ groups: ['update'] })
  @IsNotEmpty({ groups: ['create'] })
  name: string;
}

// In controller
@UsePipes(new ValidationPipe({ groups: ['create'] }))
@Post()
create(@Body() dto: UserDto) {}
```

### Global Error Format
```typescript
new ValidationPipe({
  exceptionFactory: (errors: ValidationError[]) => {
    const messages = errors.map(err =>
      Object.values(err.constraints ?? {}).join(', ')
    );
    return new BadRequestException({
      message: 'Validation failed',
      errors: messages,
    });
  },
})
```
