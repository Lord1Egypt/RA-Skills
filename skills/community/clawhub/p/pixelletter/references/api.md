# PixelLetter HTTPS API Notes

Source: PixelLetter HTTPS interface manual v1.2 (2006) and public `pixelletter.class.txt` v2.01 (2016).

## Endpoint

`POST https://www.pixelletter.de/xml/index.php`

Multipart form fields:

- `xml`: XML command payload
- `uploadfile0`, `uploadfile1`, ...: uploaded files for upload mode

The public PHP class disables TLS peer verification. Do **not** copy that behavior; keep TLS verification enabled.

## Auth block

```xml
<pixelletter version="1.3">
  <auth>
    <email>...</email>
    <password>...</password>
    <agb>ja</agb>
    <widerrufsverzicht>ja</widerrufsverzicht>
    <testmodus>1</testmodus>
    <ref></ref>
  </auth>
  ...command...
</pixelletter>
```

The PHP class effectively serializes `true` as `1` and `false` as an empty string. This skill mirrors that behavior.

## Text order

```xml
<command>
  <order type="text">
    <options>
      <action>1</action>
      <transaction></transaction>
      <control></control>
      <fax></fax>
      <location>1</location>
      <destination>DE</destination>
      <addoption></addoption>
      <returnaddress></returnaddress>
    </options>
    <text>
      <address>...</address>
      <subject>...</subject>
      <message>...</message>
    </text>
  </order>
</command>
```

## Upload order

```xml
<command>
  <order type="upload">
    <options>
      <action>1</action>
      <transaction></transaction>
      <control></control>
      <fax></fax>
      <location>1</location>
      <destination>DE</destination>
      <addoption></addoption>
      <returnaddress></returnaddress>
    </options>
  </order>
</command>
```

Attach files as `uploadfile0`, `uploadfile1`, ... . PixelLetter may convert and merge multiple files.

## Account info

```xml
<command>
  <info>
    <account:info type="all" />
  </info>
</command>
```

## Response

Typical success response:

```xml
<?xml version="1.0" encoding="iso-8859-1"?>
<pixelletter version="1.3">
  <response>
    <result code="100">
      <msg>Auftrag erfolgreich übermittelt</msg>
    </result>
    <transaction>...</transaction>
  </response>
</pixelletter>
```

Code `100` means accepted by the interface. Final send confirmation arrives by email later.

Account-info responses may use `customer:*` XML tags. Older docs showed the misspelled `costumer:*`; support both when parsing.

Error codes are documented by PixelLetter at:
`https://www.pixelletter.de/docs/error_messages.php`
