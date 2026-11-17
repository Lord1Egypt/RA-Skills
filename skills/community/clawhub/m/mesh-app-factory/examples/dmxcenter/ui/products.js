const EMPL_PRT={dlg:false,name:'',cmt:'',prefix:'',codeLen:9,isEdit:false};
export default {
inject:['service', 'tags'],
data() {return {
    products:[],
    prodInfo:cloneObj(EMPL_PRT)
}},
created(){
    this.getProducts();
},
methods:{
getProducts() {
    this.service.getProducts(true).then(products => {
        this.products=products;
    });
},
setProduct() {
    var dta=copyObj(this.prodInfo,['name','cmt','codeLen','prefix']);
    var url;
    var method;
    if(this.prodInfo.isEdit) {
        url = "/api/product/update";
        method="PUT";
        dta.id=this.prodInfo.id;
    } else {
        url = "/api/product/add";
        method="POST";
    }
    request({method:method,url:url,data:dta}, this.service.name).then(resp => {
        if(resp.code != 0) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
            return;
        }
        this.getProducts();
        this.prodInfo.dlg=false;
    })
},
rmvProduct() {
    var url="/api/product/remove?id="+this.prodInfo.id;
    request({method:"DELETE",url:url}, this.service.name).then(resp => {
        if(resp.code != 0) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
            return;
        }
        this.getProducts();
        this.prodInfo.dlg=false;
    })
},
showEdit(i) {
    var p;
    if(i>=0) {
        p=cloneObj(this.products[i]);
        p.title=this.tags.editProduct;
        p.isEdit=true;
    } else {
        p=cloneObj(EMPL_PRT);
        p.title=this.tags.addProduct;
        p.isEdit=false;
    }
    p.dlg=true;
    this.prodInfo=cloneObj(p);
}
},
template:`
<q-layout view="hHh lpr fFf">
 <q-header>
  <q-toolbar>
   <q-btn flat icon="arrow_back" dense @click="service.go_back"></q-btn>
   <q-toolbar-title>{{tags.homeMenus.prt.name}}</q-toolbar-title>
   <q-btn flat dense color="white" icon="playlist_add" @click="showEdit(-1)"></q-btn>
  </q-toolbar>
 </q-header>
<q-page-container>
    <q-page class="q-pa-md">
<q-list separator>
<q-item v-for="(p,i) in products" clickable @click="showEdit(i)">
 <q-item-section>
    <q-item-label>{{p.name}}</q-item-label>
    <q-item-label caption>{{tags.prod.prefix}}:{{p.prefix}} / {{tags.prod.codeLen}}:{{p.codeLen}}</q-item-label>
 </q-item-section>
 <q-item-section style="line-break: anywhere;">{{p.cmt}}</q-item-section>
 <q-item-section side>{{p.num}}</q-item-section>
</q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" :close="tags.close" ref="errDlg"></component-alert-dialog>

<!-- 增加/修改模板弹窗 -->
<q-dialog v-model="prodInfo.dlg" no-backdrop-dismiss>
  <q-card style="min-width:70vw">
    <q-card-section>
     <div class="text-h6">{{prodInfo.title}} {{prodInfo.name}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list>
      <q-item><q-item-section>
        <q-input v-model="prodInfo.name" :label="tags.prod.name" maxlength=30 dense></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
        <q-input v-model="prodInfo.prefix" :label="tags.prod.prefix" maxlength=30 dense></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
        <q-input v-model="prodInfo.codeLen" :label="tags.prod.codeLen" type="number" dense></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input v-model="prodInfo.cmt" :label="tags.prod.cmt" dense maxlength=300 type="textarea"></q-input>
      </q-item-section></q-item>
    </q-list>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click.stop="setProduct"></q-btn>
      <q-btn v-show="prodInfo.isEdit" flat :label="tags.remove" color="red" @click.stop="rmvProduct"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>
`
}