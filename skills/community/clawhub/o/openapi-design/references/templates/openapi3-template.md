# OpenAPI 3.0 Template

## 完整模板

```yaml
openapi: 3.0.3
info:
  title: User Management API
  description: |
    User management API for user registration, authentication, and profile management.
    
    ## Authentication
    This API uses Bearer token authentication.
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

paths:
  /users:
    get:
      summary: List users
      description: Retrieve a paginated list of users
      operationId: listUsers
      tags:
        - Users
      parameters:
        - name: page
          in: query
          description: Page number
          schema:
            type: integer
            default: 1
            minimum: 1
        - name: limit
          in: query
          description: Items per page
          schema:
            type: integer
            default: 20
            minimum: 1
            maximum: 100
        - name: status
          in: query
          description: Filter by status
          schema:
            type: string
            enum: [active, inactive, pending]
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
    
    post:
      summary: Create user
      description: Create a new user account
      operationId: createUser
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          $ref: '#/components/responses/Conflict'

  /users/{userId}:
    get:
      summary: Get user
      description: Retrieve a user by ID
      operationId: getUser
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          description: User ID
          schema:
            type: integer
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '404':
          $ref: '#/components/responses/NotFound'

    patch:
      summary: Update user
      description: Partially update a user
      operationId: updateUser
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUserRequest'
      responses:
        '200':
          description: User updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '404':
          $ref: '#/components/responses/NotFound'

    delete:
      summary: Delete user
      description: Delete a user
      operationId: deleteUser
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
      responses:
        '204':
          description: User deleted
        '404':
          $ref: '#/components/responses/NotFound'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
      properties:
        id:
          type: integer
          example: 123
        email:
          type: string
          format: email
          example: user@example.com
        name:
          type: string
          example: John Doe
        status:
          type: string
          enum: [active, inactive, pending]
          example: active
        createdAt:
          type: string
          format: date-time
          example: '2024-01-15T10:30:00Z'
        updatedAt:
          type: string
          format: date-time
          example: '2024-01-15T10:30:00Z'

    CreateUserRequest:
      type: object
      required:
        - email
        - name
        - password
      properties:
        email:
          type: string
          format: email
          example: user@example.com
        name:
          type: string
          example: John Doe
        password:
          type: string
          format: password
          minLength: 8
          example: secret123

    UpdateUserRequest:
      type: object
      properties:
        name:
          type: string
          example: John Smith
        status:
          type: string
          enum: [active, inactive]

    UserResponse:
      type: object
      properties:
        data:
          $ref: '#/components/schemas/User'

    UserListResponse:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      properties:
        total:
          type: integer
          example: 150
        page:
          type: integer
          example: 1
        limit:
          type: integer
          example: 20
        hasMore:
          type: boolean
          example: true

    Error:
      type: object
      properties:
        code:
          type: string
          example: VAL_001
        message:
          type: string
          example: Validation failed
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
                example: email
              message:
                type: string
                example: Invalid email format

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    
    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    
    Conflict:
      description: Resource conflict
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

tags:
  - name: Users
    description: User management operations
```

---

## 常用字段映射

### JSON Schema 类型映射

| JSON Type | OpenAPI Schema |
|------------|----------------|
| string | type: string |
| string (date-time) | type: string, format: date-time |
| string (email) | type: string, format: email |
| string (uuid) | type: string, format: uuid |
| number | type: number |
| integer | type: integer |
| boolean | type: boolean |
| object | type: object |
| array | type: array |

---

## 生成工具

### CLI 工具

```bash
# Redocly CLI
npx @redocly/cli lint openapi.yaml

# Spectral (lint)
npx @stoplight/spectral lint openapi.yaml

# Swagger Editor (在线)
# https://editor.swagger.org/
```

### 在线编辑器

- **Swagger Editor**: https://editor.swagger.org/
- **Redocly**: https://redocly.github.io/redoc/
- **Stoplight**: https://stoplight.io/open-source
