package lynx

import (
	"fmt"
	"io"
	"net/http"
	"net/http/cookiejar"
	"strings"

	"dodmcdund.cc/lynx-travel-agent/lynxskill/gwt"
)

func Login(remoteHost, companyCode, username, password string) (*http.Client, string, error) {
	jar, err := cookiejar.New(nil)
	if err != nil {
		return nil, "", fmt.Errorf("failed to create cookie jar: %w", err)
	}

	client := &http.Client{Jar: jar}
	body := gwt.BuildLoginBody(remoteHost, companyCode, username, password)

	req, err := http.NewRequest("POST", fmt.Sprintf("https://%s/lynx/service/security.rpc", remoteHost), strings.NewReader(body))
	if err != nil {
		return nil, "", fmt.Errorf("failed to create auth request: %w", err)
	}

	req.Header.Set("Content-Type", gwt.ContentType)

	resp, err := client.Do(req)
	if err != nil {
		return nil, "", fmt.Errorf("failed to perform auth request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, "", fmt.Errorf("auth request failed with status: %d", resp.StatusCode)
	}

	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, "", fmt.Errorf("failed to read auth response: %w", err)
	}

	if !strings.HasPrefix(string(respBody), "//OK") {
		return nil, "", fmt.Errorf("auth failed: %s", string(respBody))
	}

	for _, cookie := range resp.Cookies() {
		if cookie.Name == "JSESSIONID" {
			return client, cookie.Value, nil
		}
	}

	return nil, "", fmt.Errorf("JSESSIONID not found in response cookies")
}
