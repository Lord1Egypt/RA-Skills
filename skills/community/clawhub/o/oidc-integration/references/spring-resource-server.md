# Spring Resource Server Example

Use this reference when the user needs a concrete Spring Boot backend example for validating bearer tokens from an OIDC provider.

## When This Variant Fits

Use this variant when:

- the backend receives bearer tokens from a frontend or another client
- the app does not need to implement the browser login flow itself
- standard issuer-based JWT validation is sufficient

Prefer Spring Security resource server support over manual interceptors.

## Minimal Configuration

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://idp.example.com
```

This lets Spring discover metadata and JWKS details from the issuer.

## Example Security Configuration

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health", "/public/**").permitAll()
                .requestMatchers("/api/**").authenticated()
                .anyRequest().permitAll()
            )
            .oauth2ResourceServer(oauth -> oauth.jwt());

        return http.build();
    }
}
```

## Example Claim Access

```java
@GetMapping("/api/me")
public Map<String, Object> me(@AuthenticationPrincipal Jwt jwt) {
    return Map.of(
        "sub", jwt.getSubject(),
        "email", jwt.getClaimAsString("email")
    );
}
```

## Notes

- Validate issuer and audience requirements explicitly if the default config does not fully cover the app's needs.
- Use `JwtAuthenticationConverter` only when role or authority mapping needs customization.
- If CORS is required, configure allowed origins and headers deliberately rather than opening everything by default.
- Fall back to custom JWKS logic only for non-standard providers or unusual token formats.