# curl --silent -u 'TesLaMent963:V02&nCd5BwC7' 'https://qemu.ovh/ocs/v1.php/cloud/capabilities?format=json'

# Lister le contenu de "Documents" (profondeur 1)
# curl -u 'TesLaMent963:V02&nCd5BwC7'\
#      -X PROPFIND \
#      -H "Depth: 1" \
#      'https://qemu.ovh/remote.php/dav/files/TesLaMent963/Documents/CE/'

curl -s -u 'TesLaMent963:V02&nCd5BwC7' -X SEARCH -H "Content-Type: text/xml" -d '<?xml version="1.0" encoding="UTF-8"?>
<ns0:searchrequest xmlns:ns0="urn:ietf:params:xml:ns:caldav">
  <ns0:basicsearch>
    <ns0:select>
      <ns0:prop>
        <d:getlastmodified xmlns:d="DAV:"/>
        <d:displayname xmlns:d="DAV:"/>
        <d:href xmlns:d="DAV:"/>
      </ns0:prop>
    </ns0:select>
    <ns0:from>
      <ns0:scope>
        <ns0:depth>infinity</ns0:depth>
      </ns0:scope>
    </ns0:from>
    <ns0:where>
      <ns0:like>
        <ns0:prop>
          <d:displayname xmlns:d="DAV:"/>
        </ns0:prop>
        <ns0:literal>*facture internat Q1 2026.pdf*</ns0:literal>
      </ns0:like>
    </ns0:where>
  </ns0:basicsearch>
</ns0:searchrequest>' https://qemu.ovh/remote.php/dav/files/TesLaMent963/Documents/