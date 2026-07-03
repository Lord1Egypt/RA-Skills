package gwt

import "fmt"

func BuildLoginBody(remoteHost, companyCode, username, password string) string {
	return fmt.Sprintf(
		"7|0|9|https://%s/lynx/lynx/|4775EB021C85EC0B04470837F40FC64A|com.lynxtraveltech.common.gui.client.rpc.SecurityService|login|java.lang.String/2004016611|Z|%s|%s|%s|1|2|3|4|4|5|5|5|6|7|8|9|0|",
		remoteHost, companyCode, username, password,
	)
}

func BuildFileSearchByPartyNameBody(remoteHost, partyName string) string {
	return fmt.Sprintf(
		"7|0|9|https://%s/lynx/lynx/|521D085B722C1188DE9A385E584EB85A|com.lynxtraveltech.client.client.rpc.FileService|searchWithCount|com.lynxtraveltech.client.shared.model.FileSearchCriteria/2731823162||%s|PARTY_NAME|DD MMM YYYY|1|2|3|4|1|5|5|6|6|0|0|1|1|7|6|50|8|6|9|0|0|6|",
		remoteHost, partyName,
	)
}

func BuildFileSearchByFileReferenceBody(remoteHost, fileReference string) string {
	return fmt.Sprintf(
		"7|0|9|https://%s/lynx/lynx/|521D085B722C1188DE9A385E584EB85A|com.lynxtraveltech.client.client.rpc.FileService|searchWithCount|com.lynxtraveltech.client.shared.model.FileSearchCriteria/2731823162||%s|FILE_REFERENCE|DD MMM YYYY|1|2|3|4|1|5|5|6|7|0|0|1|1|6|6|50|8|6|9|0|0|6|",
		remoteHost, fileReference,
	)
}

func BuildRetrieveItineraryBody(remoteHost, fileIdentifier string, showCancelled bool) string {
	cancelled := 0
	if showCancelled {
		cancelled = 1
	}
	return fmt.Sprintf(
		"7|0|6|https://%s/lynx/lynx/|521D085B722C1188DE9A385E584EB85A|com.lynxtraveltech.client.client.rpc.FileService|retrieveItinerary|J|Z|1|2|3|4|4|5|6|6|6|%s|%d|0|0|",
		remoteHost, fileIdentifier, cancelled,
	)
}

func BuildFileDocumentsByTransactionReferenceBody(remoteHost, fileIdentifier, transactionIdentifier string) string {
	return fmt.Sprintf(
		"7|0|8|https://%s/lynx/lynx/|521D085B722C1188DE9A385E584EB85A|com.lynxtraveltech.client.client.rpc.FileService|getFileDocumentsAsList|J|java.lang.Long/4227064769|I|java.lang.String/2004016611|1|2|3|4|4|5|6|7|8|%s|6|%s|1|0|",
		remoteHost, fileIdentifier, transactionIdentifier,
	)
}

func BuildFileDocumentsByFileReferenceBody(remoteHost, fileIdentifier string) string {
	return fmt.Sprintf(
		"7|0|8|https://%s/lynx/lynx/|521D085B722C1188DE9A385E584EB85A|com.lynxtraveltech.client.client.rpc.FileService|getFileDocumentsAsList|J|java.lang.Long/4227064769|I|java.lang.String/2004016611|1|2|3|4|4|5|6|7|8|%s|0|1|0|",
		remoteHost, fileIdentifier,
	)
}

func BuildFileDocumentSaveBody(remoteHost, fileIdentifier, name, content, docType, attachmentURL string) string {
	return fmt.Sprintf(
		"7|0|9|https://%s/lynx/lynx/|521D085B722C1188DE9A385E584EB85A|com.lynxtraveltech.client.client.rpc.FileService|saveFileDocumentsDetails|com.lynxtraveltech.common.gui.shared.model.DocumentDetails/2779362264|%s|%s|%s|%s|1|2|3|4|1|5|5|0|1|A|0|0|0|P__________|6|7|0|%s|8|9|0|",
		remoteHost, content, docType, name, attachmentURL, fileIdentifier,
	)
}

func BuildTransactionDocumentSaveBody(remoteHost, fileIdentifier, transactionIdentifier, name, content, docType, attachmentURL string) string {
	return fmt.Sprintf(
		"7|0|10|https://%s/lynx/lynx/|521D085B722C1188DE9A385E584EB85A|com.lynxtraveltech.client.client.rpc.FileService|saveFileDocumentsDetails|com.lynxtraveltech.common.gui.shared.model.DocumentDetails/2779362264|java.lang.Long/4227064769|%s|%s|%s|%s|1|2|3|4|1|5|5|6|%s|1|A|0|0|0|P__________|7|8|0|%s|9|10|0|",
		remoteHost, content, docType, name, attachmentURL, transactionIdentifier, fileIdentifier,
	)
}
