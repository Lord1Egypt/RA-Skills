package main

import "fmt"

const contentType = "text/x-gwt-rpc; charset=utf-8"

const (
	gwtTypeArray               = "java.util.ArrayList"
	gwtTypeBigDecimal          = "java.math.BigDecimal"
	gwtTypeSQLDate             = "java.sql.Date"
	gwtTypeJavaDate            = "java.util.Date"
	gwtTypeDouble              = "java.lang.Double"
	gwtTypeLong                = "java.lang.Long"
	gwtTypeString              = "java.lang.String"
	gwtTypeFileSearchResults   = "com.lynxtraveltech.client.shared.model.FileSearchResults"
	gwtTypeFileSummary         = "com.lynxtraveltech.client.shared.model.FileSummary"
	gwtTypeTransactionSummary  = "com.lynxtraveltech.client.shared.model.TransactionSummary"
	gwtTypeDocumentDetails     = "com.lynxtraveltech.common.gui.shared.model.DocumentDetails"
)

func buildGWTLoginBody(host, companyCode, username, password string) string {
	return fmt.Sprintf("7|0|9|https://%s/lynx/lynx/|4775EB021C85EC0B04470837F40FC64A|com.lynxtraveltech.common.gui.client.rpc.SecurityService|login|java.lang.String/2004016611|Z|%s|%s|%s|1|2|3|4|4|5|5|5|6|7|8|9|0|",
		host, companyCode, username, password)
}

func buildFileSearchByPartyNameGWTBody(host, partyName string) string {
	return fmt.Sprintf("7|0|9|https://%s/lynx/lynx/|521D085B722C1188DE9A385E584EB85A|com.lynxtraveltech.client.client.rpc.FileService|searchWithCount|com.lynxtraveltech.client.shared.model.FileSearchCriteria/2731823162||%s|PARTY_NAME|DD MMM YYYY|1|2|3|4|1|5|5|6|6|0|0|0|1|7|6|50|8|6|9|0|0|6|",
		host, partyName)
}

func buildFileSearchByFileReferenceGWTBody(host, fileReference string) string {
	return fmt.Sprintf("7|0|9|https://%s/lynx/lynx/|521D085B722C1188DE9A385E584EB85A|com.lynxtraveltech.client.client.rpc.FileService|search|com.lynxtraveltech.client.shared.model.FileSearchCriteria/2731823162||%s|PARTY_NAME|DD MMM YYYY|1|2|3|4|1|5|5|6|7|0|1|1|6|6|50|8|6|0|9|0|0|6|",
		host, fileReference)
}

func buildFileDocumentsByTransactionReferenceGWTBody(host, fileIdentifier, transactionIdentifier string) string {
	return fmt.Sprintf("7|0|8|https://%s/lynx/lynx/|521D085B722C1188DE9A385E584EB85A|com.lynxtraveltech.client.client.rpc.FileService|getFileDocumentsAsList|J|java.lang.Long/4227064769|I|java.lang.String/2004016611|1|2|3|4|4|5|6|7|8|%s|6|%s|1|0|",
		host, fileIdentifier, transactionIdentifier)
}

func buildFileDocumentSaveGWTBody(host, fileIdentifier, name, content, documentType, attachmentURL string) string {
	return fmt.Sprintf("7|0|9|https://%s/lynx/lynx/|521D085B722C1188DE9A385E584EB85A|com.lynxtraveltech.client.client.rpc.FileService|saveFileDocumentsDetails|com.lynxtraveltech.common.gui.shared.model.DocumentDetails/2779362264|%s|%s|%s|%s|1|2|3|4|1|5|5|0|1|A|0|0|0|P__________|6|7|0|%s|8|9|0|",
		host, content, documentType, name, attachmentURL, fileIdentifier)
}

func buildTransactionDocumentSaveGWTBody(host, fileIdentifier, transactionIdentifier, name, content, documentType, attachmentURL string) string {
	return fmt.Sprintf("7|0|10|https://%s/lynx/lynx/|521D085B722C1188DE9A385E584EB85A|com.lynxtraveltech.client.client.rpc.FileService|saveFileDocumentsDetails|com.lynxtraveltech.common.gui.shared.model.DocumentDetails/2779362264|java.lang.Long/4227064769|%s|%s|%s|%s|1|2|3|4|1|5|5|6|%s|1|A|0|0|0|P__________|7|8|0|%s|9|10|0|",
		host, content, documentType, name, attachmentURL, transactionIdentifier, fileIdentifier)
}

func buildRetrieveItineraryGWTBody(host, fileIdentifier string) string {
	return fmt.Sprintf("7|0|6|https://%s/lynx/lynx/|521D085B722C1188DE9A385E584EB85A|com.lynxtraveltech.client.client.rpc.FileService|retrieveItinerary|J|Z|1|2|3|4|4|5|6|6|6|%s|0|0|0|",
		host, fileIdentifier)
}
