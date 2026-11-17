# informat.codec Encoding and Decoding

## Overview

Use `informat.codec` to perform encoding, decoding, signing, and other functions.

## hash

Get the hash value of a string

```javascript
informat.codec.hash(str, method)
```

| Parameter     | Type     | Description                                                          |
|--------|--------|-------------------------------------------------------------|
| str    | `String` | The string to compute the hash value for                                                  |
| method | `String` | Hash function. Available methods: `md5`, `sha1`, `sha256`, `sha224`, `sha384`, `sha512` |

**Return Value**

Type `String`, returns the hash value of str

**Example**

::: code-group

```javascript [Call]
informat.codec.hash('hello informat', 'md5');
console.log(md5Result);
```

```text [Return Value]
6de76e2f68123fd1a06b86a5dabca022
```
:::

## base64Encode

Get the base64 encoding of a string

```javascript
informat.codec.base64Encode(str)
```

| Parameter  | Type     | Description      |
|-----|--------|---------|
| str | `String` | The string to encode |

**Return Value**

Type `String`, returns the base64 value of str

**Example**

::: code-group

```javascript [Call]
informat.codec.base64Encode('hello informat');
```

```text [Return Value]
aGVsbG8gaW5mb3JtYXQ=
```
:::

## base64EncodeToBytes

Get the base64 encoding of a string as bytes

```javascript
informat.codec.base64EncodeToBytes(str)
```

| Parameter  | Type     | Description      |
|-----|--------|---------|
| str | `String` | The string to encode |

**Return Value**

Type `Array<Byte>`, returns the base64 value of str

**Example**

::: code-group

```javascript [Call]
informat.codec.base64EncodeToBytes('hello informat');
```

```text [Return Value]
"YUdWc2JHOGdhVzVtYjNKdFlYUT0="
```
:::

## base64Decode

Return the byte array after base64 decoding

```javascript
informat.codec.base64Decode(str)
```

| Parameter  | Type     | Description           |
|-----|--------|--------------|
| str | `String` | Base64 encoded string |

**Return Value**

Type is `Array<Byte>`, returns the base64 decoded value of str

**Example**

::: code-group

```javascript [Call]
informat.codec.base64Decode('aGVsbG8gaW5mb3JtYXQ=');
```
```text [Return Value]
'aGVsbG8gaW5mb3JtYXQ='
```
:::

## base64DecodeToString

Return the string after base64 decoding

```javascript
informat.codec.base64DecodeToString(str)
```

| Parameter  | Type     | Description           |
|-----|--------|--------------|
| str | `String` | Base64 encoded string |

**Return Value**

Type is `String`, returns the base64 decoded string of str

**Example**

::: code-group

```javascript [Call]
informat.codec.base64DecodeToString('aGVsbG8gaW5mb3JtYXQ=');
```

```text [Return Value]
'hello informat'
```
:::

## base64DecodeFromBytes

Return the byte array after base64 decoding from bytes

```javascript
informat.codec.base64DecodeFromBytes(bytes)
```

| Parameter  | Type     | Description           |
|-----|--------|--------------|
| bytes | `Array<Byte>` | Base64 encoded byte array |

**Return Value**

Type is `Array<Byte>`, returns the base64 decoded value

**Example**

::: code-group

```javascript [Call]
const encode = informat.codec.base64EncodeToBytes('hello informat');
const decode = informat.codec.base64DecodeFromBytes(encode);
```

```text [Return Value]
aGVsbG8gaW5mb3JtYXQ=
```
:::

## sign

Sign a string using a signing algorithm

```javascript
informat.codec.sign(str, method, privateKey)
```

| Parameter         | Type     | Description         |
|------------|--------|------------|
| str        | `String` | The string to sign  |
| method     | `String` | Signing method       |
| privateKey | `String` | RSA private key for signing |

::: info Supported signing method types:
- MD2withRSA
- MD5withRSA
- SHA1withRSA
- SHA224withRSA
- SHA256withRSA
- SHA384withRSA
- SHA512withRSA
- MD5andSHA1withRSA
:::

**Return Value**

Type `String`, returns the signing result of str


**Example**

::: code-group

```javascript [Call]
const privateKey = '<rsa-private-key-base64>';
const signResult = informat.codec.sign('hello world', 'SHA256withRSA', privateKey);
```

```text [Return Value]
<rsa-signature-base64>
```
:::

## rsaEncryptHexByPrivateKey

RSA private key encryption (returns hexadecimal string) (typically used for signing)

```javascript
informat.codec.rsaEncryptHexByPrivateKey(data, privateKey)
```

| Parameter  | Type     | Description      |
|-----|--------|---------|
| data | `String` | Data |
| privateKey | `String` | Private key |

**Return Value**

Type `String`, returns the RSA encrypted value of data


## rsaEncryptBase64ByPrivateKey

RSA private key encryption (returns Base64 encoded string) (typically used for signing)

```javascript
informat.codec.rsaEncryptBase64ByPrivateKey(data, privateKey)
```

| Parameter  | Type     | Description      |
|-----|--------|---------|
| data | `String` | Data |
| privateKey | `String` | Private key |

**Return Value**

Type `String`, returns the RSA encrypted value of data


## rsaEncryptHexByPublicKey

RSA public key encryption (returns hexadecimal string) (used for data protection)

```javascript
informat.codec.rsaEncryptHexByPublicKey(data, publicKey)
```

| Parameter  | Type     | Description      |
|-----|--------|---------|
| data | `String` | Data |
| publicKey | `String` | Public key |

**Return Value**

Type `String`, returns the RSA encrypted value of data


## rsaEncryptBase64ByPublicKey

RSA public key encryption (returns Base64 encoded string) (used for data protection)

```javascript
informat.codec.rsaEncryptBase64ByPublicKey(data, publicKey)
```

| Parameter  | Type     | Description      |
|-----|--------|---------|
| data | `String` | Data |
| publicKey | `String` | Public key |

**Return Value**

Type `String`, returns the RSA encrypted value of data


## rsaDecryptByPublicKey

RSA public key decryption (typically used for signature verification)

```javascript
informat.codec.rsaDecryptByPublicKey(data, publicKey)
```

| Parameter  | Type     | Description      |
|-----|--------|---------|
| data | `String` | Encrypted data |
| publicKey | `String` | Public key |

**Return Value**

Type `String`, returns the RSA decrypted value of the encrypted data


## rsaDecryptByPrivateKey

RSA private key decryption

```javascript
informat.codec.rsaDecryptByPrivateKey(data, privateKey)
```

| Parameter  | Type     | Description      |
|-----|--------|---------|
| data | `String` | Encrypted data |
| privateKey | `String` | Private key |

**Return Value**

Type `String`, returns the RSA decrypted value of the encrypted data

## generateRSAKey

Generate an RSA key pair (including public key and private key)

```javascript
informat.codec.generateRSAKey()
```


**Return Value**

Type Map<String, String>, returns a map object containing the public key and private key


```js
const keyPair = informat.codec.generateRSAKey();
console.log('Public Key:', keyPair.publicKeyBase64);
console.log('Private Key:', keyPair.privateKeyBase64);
```

## tripleDESEncrypt
3DES encryption
```javascript
informat.codec.tripleDESEncrypt(data, base64Key)
```
| Parameter  | Type     | Description      |
|-----|--------|---------|
| data | `String` | Data to encrypt |
| base64Key | `String` | Base64 encoded key |
**Return Value**
Type `String`, returns the 3DES encrypted value of data

## tripleDESDecrypt
3DES decryption
```javascript
informat.codec.tripleDESDecrypt(base64Data, base64Key)
```
| Parameter  | Type     | Description      |
|-----|--------|---------|
| base64Data | `String` | Base64 encoded encrypted data |
| base64Key | `String` | Base64 encoded key |
**Return Value**
Type `String`, returns the 3DES decrypted value of the encrypted data base64Data
